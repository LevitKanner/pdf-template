import base64

from playwright.async_api import async_playwright


def image_to_base64(image_path) -> str:
    print("converting to base64... ")
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/{image_path.split('.')[-1]};base64,{encoded_string}"


async def generate_pdf_playwright(*, document_title: str, data: list[dict[str, str]] | None = None) -> bytes:
    # Go get images to render, I had to convert the image to base64
    image_src = image_to_base64("wave-logo.png")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{document_title}</title>
        <style>
            @page {{
                size: A4; 
                margin: 1cm 0 2cm 0; 
                counter-increment: page;
                page-break-after: always;
            }}
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                border-top: .25pt solid #666;
                font-size: 9pt;
                width: 50%;
            }}
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                color: rgb(31 41 55);
            }}
            html, body {{
                min-height: 100%;
            }}

            header {{
                display: flex;
                justify-content: space-between;
                padding: 5px 0;
            }}
            .report-info {{
                display: flex;
                flex-direction: column;
                gap: 5px;
            }}
            .tx {{
                display: flex;
                flex-direction: column;
                padding: 12px 16px;
                border-bottom: 0.2px solid #000;
            }}
            .tx-hd {{
                display: flex;
                justify-content: space-between;
                padding-bottom: 6px;
                border-bottom: 0.2px solid #000;
            }}
            .tx-hd-it {{
                display: flex;
                flex-direction: column;
            }}
            .tx-body {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 6px;
                margin-top: 12px;
            }}
            .tx-body div {{
                display: flex;
                flex-direction: column;
                gap: 2px;
            }}
            .label {{
                font-size: 14px;
            }}
            .value {{
                font-size: 14px;
                font-weight: 600;
            }}
            .hd-value {{
                font-size: 18px;
                font-weight: 700;
            }}
            .merchant-name {{
                font-size: 24px;
                font-weight: 700;
            }}
            #body {{
                border: 0.2px solid #000;
            }}
        </style>
    </head>
    <body>
        <div class="root">
            <header>
                <div id="logo">
                    <img src="{image_src}" alt="Wave Logo" style="height: 80px;">
                </div>
                <div class="report-info">
                    <p class="merchant-name"> Anna's Apiaries</p>
                    <p class="value"> 20232j</p>
                    <p class="value"> 2024-01-01 to 2024-03-01</p>
                </div>
            </header>
            <div id="body">
                {"".join((f""" 
                <div> 
                    <div class="tx">
                        <div class="tx-hd">
                            {"".join(f"""
                                <div class="tx-hd-it">
                                    <p class="label">{k}</p>
                                    <p class="value">{v}</p>
                                </div>
                            """ for (k, v) in list(tx.items())[:3])}
                        </div>
                        <div class="tx-body">
                            {"".join(f"""
                                <div class="normal">
                                    <p class="label">{k}</p>
                                    <p class="value">{v}</p>
                                </div>
                            """ for (k, v) in list(tx.items())[3:])}
                        </div>
                    </div>
                </div>
                """ for tx in data))}
            </div>
        </div>
    </body>
    </html>
    """

    # The footer template on each page of the pdf
    footer = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .footer {
                padding-right: 1cm;
                padding-left: 1cm;
                display: flex;
                justify-content: space-between;
                align-items: end;
                font-size: 8px;
                color: #000;
                text-align: center;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <div class="footer">
            <div></div>
            <div style="display: flex; flex-direction: column; align-items: center;">
                <span>wave mobile money</span>
                <span>P.O.Box 15526</span>
                <a href="mailto:wave@gmail.com">wave email</a>
            </div>
            <div>
                <span class="pageNumber"></span> of <span class="totalPages"></span>
            </div>
        </div>
    </body>
    </html>
    """

    # The header template on each page of the pdf, shows the date the pdf was generated
    header = ("<div style='font-size: 10px; color: #000; text-align: end; width: 100%; padding-right:1cm; "
              "padding-left:1cm;'><span class='date'></span></div>")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.set_content(html_content)
        await page.emulate_media(media="screen")
        pdf_bytes = await page.pdf(header_template=header,
                                   footer_template=footer,
                                   scale=0.6, tagged=True,
                                   display_header_footer=True)

        await browser.close()

        return pdf_bytes

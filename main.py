import asyncio
import time

from pdf import generate_pdf_playwright

# Number of report entries to generate, you can modify this number to see how long it takes to generate the PDF
num_of_entries = 1000

data = [
    {
        "timestamp": "2022-08-16 14:02:06",
        "tx_id": "T_JW3N2XG2ZI",
        "group_id": "PB_jD9xl0oKVeTF",
        "telephone": "+221765550001",
        "amount": "-1000",
        "currency": "CFA",
        "summary": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quos.",
        "nat_id": "+221765550001",
        "fee": "-100",
        "balance": "50990",
        "reference": "Lorem ipsum dolor sit, amet consectetur adipisicing elit.",
        "customer_name": "John Doe",
        "gross_amount": "-1010",
        "cashier_name": "Bob Buyer",
        "reason": "Lorem ipsum dolor sit amet consectetur,"
    }
    for _ in range(num_of_entries)
]

start = time.time()

pdf_bytes = asyncio.new_event_loop().run_until_complete(
    generate_pdf_playwright(document_title="Merchant Report", data=data))

with open("merchant_report_playwright.pdf", "wb") as f:
    f.write(pdf_bytes)

end = time.time()
print(f"Took: {end - start} seconds to generate the PDF with playwright.")
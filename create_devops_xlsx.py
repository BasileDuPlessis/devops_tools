import openpyxl

# Create a new workbook and select the active worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Set the title of the worksheet
worksheet.title = 'DevOps DORA'

# Define headers for the DORA metrics
headers = ['Metric', 'Value', 'Formula']

# Add headers to the first row
worksheet.append(headers)

# Add DORA metrics data (example data)
metrics = [
    ['Deployment Frequency', '', '=COUNTA(A2:A100)'],
    ['Lead Time for Changes', '', '=AVERAGE(B2:B100)'],
    ['Mean Time to Restore', '', '=AVERAGE(C2:C100)'],
    ['Change Failure Rate', '', '=(COUNTIF(D2:D100, "Fail") / COUNTA(D2:D100)) * 100']
]

# Append the metrics data to the worksheet
for metric in metrics:
    worksheet.append(metric)

# Save the workbook to a file
workbook.save('devops-dora-template.xlsx')

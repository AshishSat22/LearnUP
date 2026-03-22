import os
import urllib.request
import ssl

BASE = os.path.dirname(os.path.abspath(__file__))
PAPERS_DIR = os.path.join(BASE, "static", "papers")
os.makedirs(PAPERS_DIR, exist_ok=True)

# Disable SSL verification for nic.in links if needed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

YEARS = ["2023_24", "2022_23", "2021_22", "2020_21", "2019_20", "2018_19"]
SUBJECTS = ["Physics", "Chemistry", "Maths"]

# Dummy PDF generator in case network fails
def create_dummy_pdf(path, text):
    dummy_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> >>\nendobj\n4 0 obj\n<< /Length 53 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Failed to download. Offline Dummy PDF.) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000122 00000 n\n0000000288 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n393\n%%EOF\n"
    with open(path, "wb") as f:
        f.write(dummy_content)

def main():
    print("Downloading Official CBSE Papers for multiple years...")
    
    for subject in SUBJECTS:
        sub_dir = os.path.join(PAPERS_DIR, subject)
        os.makedirs(sub_dir, exist_ok=True)
        
        for year in YEARS:
            base_url = f"https://cbseacademic.nic.in/web_material/SQP/ClassXII_{year}"
            
            # They change casing sometimes, but usually it's Physics-SQP.pdf
            urls = {
                "SQP": f"{base_url}/{subject}-SQP.pdf",
                "MS": f"{base_url}/{subject}-MS.pdf"
            }
            
            for ptype, url in urls.items():
                # Save as e.g. 2023_24-SQP.pdf
                path = os.path.join(sub_dir, f"{year}-{ptype}.pdf")
                try:
                    print(f"Fetching {subject} {year} {ptype}...")
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, context=ctx) as response:
                        with open(path, "wb") as f:
                            f.write(response.read())
                    print(f"✅ Saved {path}")
                except Exception as e:
                    print(f"❌ Failed to download {url}: {e}")
                    print(f"Generating dummy local PDF for {subject} {year} {ptype} instead...")
                    create_dummy_pdf(path, f"Dummy offline PDF {subject} {year} {ptype}")

    print("Download cycle complete.")

if __name__ == "__main__":
    main()

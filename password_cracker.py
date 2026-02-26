import zipfile

def main():
    zip_filename = 'whitehouse_secrets.zip'
    dictionary_file = 'Ashley-Madison.txt'
    
   
    try:
        with open(dictionary_file, 'r', encoding='utf-8', errors='ignore') as f:
            
            passwords = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: {dictionary_file} not found.")
        return

 
    print(f"Starting brute force on {zip_filename}...")
    
    count = 0
    with zipfile.ZipFile(zip_filename) as zf:
        for password in passwords:
            count += 1
            
            
            if count % 10000 == 0:
                print(f"Iteration {count}: Trying '{password}'...")

            try:
                zf.extractall(pwd=bytes(password, 'utf-8'))
                
                
                print("-" * 30)
                print(f"SUCCESS! Password found: {password}")
                print("-" * 30)
                break 
                
            except (RuntimeError, zipfile.BadZipFile, Exception):
                continue

if __name__ == "__main__":
    main()
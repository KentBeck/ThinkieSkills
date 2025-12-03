import csv
import os
import shutil

def main():
    posts_dir = "Substack download 30.11.2025/posts"
    output_dir = "thinkie_htmls"
    csv_path = "Substack download 30.11.2025/posts.csv"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row['title']
            if 'thinkie' in title.lower():
                post_id = row['post_id']
                filename = f"{post_id}.html"
                source_path = os.path.join(posts_dir, filename)
                dest_path = os.path.join(output_dir, filename)

                if os.path.exists(source_path):
                    shutil.copy2(source_path, dest_path)
                    print(f"Copied: {filename}")
                    count += 1
                else:
                    # Try finding the file if the post_id in CSV doesn't match filename exactly
                    # Sometimes filenames are truncated or slightly different
                    found = False
                    for f in os.listdir(posts_dir):
                        if f.startswith(post_id.split('.')[0]): # Match by ID prefix
                             if f.endswith(".html"):
                                source_path = os.path.join(posts_dir, f)
                                dest_path = os.path.join(output_dir, f)
                                shutil.copy2(source_path, dest_path)
                                print(f"Copied (fuzzy match): {f}")
                                count += 1
                                found = True
                                break
                    if not found:
                        print(f"File not found: {filename}")

    print(f"Total Thinkies copied: {count}")

if __name__ == "__main__":
    main()

import os
import math

def merge_into_chunks(directory, num_chunks):
    md_files = sorted([f for f in os.listdir(directory) if f.endswith('.md')])
    total_files = len(md_files)
    # Determine the chunk size; use math.ceil to ensure all files are included
    chunk_size = math.ceil(total_files / num_chunks)
    
    for i in range(num_chunks):
        # Slice the list for this chunk
        chunk_files = md_files[i*chunk_size : (i+1)*chunk_size]
        if not chunk_files:
            break
        output_file = os.path.join(directory, f"merged_chunk_{i+1}.md")
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for fname in chunk_files:
                file_path = os.path.join(directory, fname)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(f"# {fname}\n\n")
                    outfile.write(content)
                    outfile.write("\n\n---\n\n")
        print(f"Merged {len(chunk_files)} files into '{output_file}'")

if __name__ == '__main__':
    directory = "downloaded_md_files"  # folder with markdown files
    num_chunks = 10                   # desired number of merged files
    merge_into_chunks(directory, num_chunks)

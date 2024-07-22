from tqdm import tqdm

def divide_range_and_generate_files(start_range, end_range, public_key, num_files):
    # Convert hex ranges to integers
    start = int(start_range, 16)
    end = int(end_range, 16)
    
    # Calculate the range for each file
    total_range = end - start + 1
    range_per_file = total_range // num_files
    
    for i in tqdm(range(1, num_files + 1)):
        part_start = start + (i - 1) * range_per_file
        part_end = start + i * range_per_file - 1 if i < num_files else end
        
        filename = f"chave/130-{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"{hex(part_start)[2:]}\n")
            f.write(f"{hex(part_end)[2:]}\n")
            f.write(f"{public_key}\n")

# Parameters
start_range = "200000000000000000000000000000000"
end_range = "3ffffffffffffffffffffffffffffffff"
public_key = "03633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852"
num_files = 5000000

# Call the function
divide_range_and_generate_files(start_range, end_range, public_key, num_files)

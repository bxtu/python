def letter_frequency_analysis(text, sample_size):
    text = text[:sample_size].lower()  
    total_letters = sum(char.isalpha() for char in text)    
    # 82
    letter_frequencies = {}
    for char in text:
        if char.isalpha():
            if char in letter_frequencies:
                letter_frequencies[char] += 1
            else:
                letter_frequencies[char] = 1

    for char, count in letter_frequencies.items():
        frequency = (count / total_letters) * 100
        print(f"{char}: number of using: {count}  using rate: {frequency:.4f}")
        letter_frequencies[char] = frequency  # Store frequency in the dictionary


    return letter_frequencies
        


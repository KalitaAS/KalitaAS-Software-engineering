def read_file():
    with open("./HW1 V8/first_task.txt", encoding="utf-8") as file:
        return file.readlines()

def text_to_words(lines):
    words = []
    for line in lines:
        _line = (line
                 .replace("'", "")
                 .replace("?", "")
                 .replace("!", "")
                 .replace(".", "")
                 .replace("-", " ")
                 .replace(",", " ")
                 .lower().strip())
        words += _line.split()
    return words

def calc_freq(words):
    word_freq = {}
    for word in words:
        if len(word) == 0:
            continue
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

def write_to_file(stat):
    with open("first_task_result.txt", "w", encoding="utf-8") as file:
        for key, val in stat:
            file.write(f"{key}:{val}\n")

def avg_words_per_sentence(lines, words):
    text = " ".join(lines)
    sentences = 0
    for char in text: 
        if char in '.!?': 
            sentences += 1
    return len(words) / sentences 

def write_to_file_avg_words(avg_words):
    with open("first_task_avg.txt", "w", encoding="utf-8") as file:
        file.write(f"{avg_words:.2f}\n")  

lines = read_file()
words = text_to_words(lines)
word_freq = calc_freq(words)
write_to_file(word_freq)

avg_words = avg_words_per_sentence(lines, words)
write_to_file_avg_words(avg_words)

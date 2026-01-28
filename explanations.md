# HW1-w26

## Part 1

### Correctness: Describe how your scanner extensions implement the required behavior, including any edge cases you handled.

My scanner extensions helped implement token matching functionlity for semicolons, increement, addition, multiplication, assignment, IDs, and numbers with an optional single decimal point. It handles edge cases like ill formatted IDs like "1a" and numbers with invalid decimal points (i.e. "123." or "."). It scans tokens from left to right, prefers the longest match for INCR, returns None when there is no more input, and raises ScannerException if there are any unrecognized characters. 

### Conceptual: Explain how your implementation aligns with the naive scanner design.

My implementation aligns with the naive scanner design by using a StringStream with peek_char and eat_char to scan left-to-right without regex. It skips any whitespace before matching and performs simple character comparisons and greedy consumption for each type of token.


### Experiments: Report your timing results for 10/100/1000/10000 tokens and how you ran them.

For 10 tokens, I ran `python3 part1/NaiveScanner.py tests/test10.txt`, and it took around 0.0003s.
For 100 tokens, I ran `python3 part1/NaiveScanner.py tests/test100.txt`, and it took around 0.0015s.
For 1000 tokens, I ran `python3 part1/NaiveScanner.py tests/test1000.txt`, and it took around 0.0172s. 
For 10000 tokens, I ran `python3 part1/NaiveScanner.py tests/test10000.txt`, and it took around 0.0884s.

### Explanation: Summarize your implementation choices and discuss performance.

To satisfy the no regex constraint, I chose explicit character checks because it was the simplest. I implemented INCR to prefer the longest match, and fall back to PLUS if necessary. To ensure the proper formatting for IDs, I check the first letter, then loop over letters/digits to ensure that there are no digits before the first letter. For NUM, I track a single optional dot and ensure that there are digits after the dot so that leading dot numbers are handled. The performance scales roughly linearly with the number of tokens due to single pass, constant-time checks for each character and token.

## Part 2

### Submission: Summarize what you submitted in tokens.py and where it lives in your repo.

My tokens.py file lives under the part2 folder and it defines all required tokens and a keyword remap using `id_action`.

### Written Report: Describe your RE definitions and include timing results for the EM scanner.

For ID, my RE definition is `[A-Za-z][A-Za-z0-9]*` ad it matches letters, then letters/digits, and it cannot start with a digit.
For NUM, my RE definition is `(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)` and it matches integer or decimal, allows leading dot, and requires digits after dot.
For HNUM, my RE definition is `0[xX][0-9a-fA-F]+` and it matches hex (letters a-f) and is case-insensitive.
- For all of the operatorsa and punct, my RE definitions are `\+\+`, `\+`, `\*`, `;`, `\(`, `\)`, `\{`, `\}`, `=` and they match the corresponding symbol.
For IGNORE, my RE definition is `[ \t\n]+` and it skips any whitespaces or newlines.
For the token actions, `if`, `else`, `while`, `int`, `float`, they are mapped in `id_action`.

For 10 tokens, I ran `python3 part2/EMScanner.py tests/test10.txt`, and it took around 0.0138s.
For 100 tokens, I ran `python3 part2/EMScanner.py tests/test100.txt`, and it took around 1.5916s.
For 1000 tokens, I ran `python3 part2/EMScanner.py tests/test1000.txt`, and it took around 177.0410s.
For 10000 tokens, I ran `python3 part2/EMScanner.py tests/test10000.txt`, and it took multiple hours. I ran the test around 11am and it was still running by 5pm, so I just stopped the test. 

### Testing and Verification: Explain how you tested part2.txt (locally and on Gradescope) and report the outcomes.

I tested part2.txt by checking inputs with IDs, decimals, hex, operators, parentheses, braces, and keywords. I made sure that IGNORE removed whitespaces and newlines. I also submitted on Gradescope to make sure it passed all the tests. 

### Debugging and Iteration: Describe any failures you encountered and how you resolved them (include submission iterations if relevant).

The only failure I encountered was with NUM and I had to make sure that it correctly matched numbers with decimals (i.e. `0.1` is allowed but not `56.`). I resolved this by requiring at least one digit after the dot in my regular expression. 

## Part 3

### Correctness: Describe how your SOS scanner implements the required behavior, including tricky cases.

My SOS scanner implements the required behavior by using re.match for the start of any remaining input in each token regex, then takes the longest match, applies the token action, takes the return value, and skips any IGNORE tokens. For the tricky cases, like “++” vs “+”, I resolved it by choosing the longest match. Other cases included invalid decimal inputs like “56.” or “.”, which I handled by raising a ScannerException. 

### Conceptual: Explain how your design matches the SOS scanning approach.

My design matches the SOS scanning approach by checking each token pattern once per token() call through start-of-string matching rather than rather than trying all the substrings. Selecting the longest match selection ensures that the behavior is deterministic for patterns that overlap. This design is the same as the SOS model, which tries to match from the current position, then consumes.

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the EM scanner.

For 10 tokens, I ran `python3 part3/SOSScanner.py tests/test10.txt`, and it took around 0.0004s. 
For 100 tokens, I ran `python3 part3/SOSScanner.py tests/test100.txt`, and it took around 0.0015s
For 1000 tokens, I ran `python3 part3/SOSScanner.py tests/test1000.txt`, and it took around 0.0129s.
For 10000 tokens, I ran `python3 part3/SOSScanner.py tests/test10000.txt`, and it took around 0.2025s.

Compared to the EM scanner, the SOS scanner is a lot faster, especially after 100 tokens. 

### Explanation: Summarize implementation details and performance observations.

My implementation selects the longest start-of-string match, applies actions and keyword remaps, consumes exactly what was returned, and skips IGNORE. The performance scales roughly linearly with input size and is much faster than the EM scanner. 

## Part 4

### Correctness: Describe how your NG scanner implements the required behavior, including tricky cases.

My NG scanner builds one master regex with named groups for every token, adds it to the start of the input, matches once per token(), applies the token’s action, consumes len(ret.value), and skips IGNORE. The tricky cases, like pattern overlaps, are resolved by pattern order in the alternation (i.e. INCR before PLUS). 

### Conceptual: Explain how your design matches the NG scanning approach.

My design matches the NG approach by using a single compiled start-of-string regex for all tokens. It uses named groups to identify which token is matched and creates one regex match per token. It is consistent with the behavior of the SOS scanner but is more efficient because of the combined matching.

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the SOS scanner.

For 10 tokens, I ran `python3 part4/NGScanner.py tests/test10.txt`, and it took around 3.3855s.
For 100 tokens, I ran `python3 part4/NGScanner.py tests/test100.txt`, and it took around 0.0002s
For 1000 tokens, I ran `python3 part4/NGScanner.py tests/test1000.txt`, and it took around 0.0028s.
For 10000 tokens, I ran `python3 part4/NGScanner.py tests/test10000.txt`, and it took around 0.1004s. 

Compared to the SOS scanner, the NG scanner is faster for larger inputs but slower for smaller inputs.

### Explanation: Summarize implementation details and performance observations.

I implemented the master regex by creating it once during initialization using named groups and ^ anchoring. It then gets reused to minimizing compilation and match attempts. Overlaps are resolved by ordering alternatives so that specific patterns come first (i.e matching “++” before “+”). For larger inputs, the performance scales linearly and is slightly faster than the SOS scanner. 


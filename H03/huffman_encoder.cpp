#include <string>
#include <vector>

#include <sstream>
#include <fstream>
#include <iostream>
#include <locale>
#include <codecvt>

using namespace std;

wstring alphabets = L"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

/*
	 Processes a single word and returns tokens in that.
	 There could be special symbols in the beginning or end
	 and these are treated as their own tokens.
	 This is called by get_tokens.
*/
vector<wstring> process_word(wstring word) {
	vector<wstring> frontlist;
	int i = 0;
	while (i < word.size() && alphabets.find(word[i]) == wstring::npos) {
		wstring t(1, word[i]);
		frontlist.push_back(t);
		i++;
	}
	
	vector<wstring> endlist;
	int j = word.size() - 1;
	int start = i;
	while (j >= i && alphabets.find(word[j]) == string::npos) {
		wstring t(1, word[j]);
		endlist.insert(endlist.begin(), t);
		j--;
	}

	wstring words = L"";
	if (i <= j) {
		words = word.substr(i, (j - i) + 1);
	}
	vector<wstring> finallist;
	if (!frontlist.empty()) {
		for (wstring st : frontlist) {
			finallist.push_back(st);
		}
	}
	if (words != L"") {
		finallist.push_back(words);
	}
	if (!endlist.empty()) {
		for (wstring st : endlist) {
			finallist.push_back(st);
		}
	}
	return finallist;
}

/*
	 Gets a filename as input, and returns a vector of tokens. Each token is 
	 represented as a wstring object in order to preserve its unicode
	 encoding.
	 Use wstring objects in your program instead of strings. They behave the same
	 way and have the same set of functions.
*/
vector<wstring> get_tokens(string inpfile) {
	vector<wstring> tokens;

	locale mylocale("en_US.UTF8");
	cout.imbue(mylocale);
	cin.imbue(mylocale);
	
	std::locale utf8_locale(mylocale, new std::codecvt_utf8<wchar_t>);

	std::wifstream win;
	win.imbue(utf8_locale);
	win.open(inpfile);

	std::wstring line;

	while (getline(win, line)) {
		line.append(wstring(L"\n"));
		vector<wstring> spacedwords;
		wstring temp;
		wstringstream t2;
		t2.str(line);
		while (getline(t2, temp, L' ')) {
			spacedwords.push_back(temp);
		}
		for (wstring word : spacedwords) {
			if (word == L"") {
				tokens.push_back(L" ");
				continue;
			}
			vector<wstring> tokenized = process_word(word);
			for (wstring token : tokenized) {
				tokens.push_back(token);
			}
			if (tokenized[tokenized.size() - 1] != L"\n") {
				tokens.push_back(L" ");
			}
		}
	}
	win.close();
	return tokens;
}

// You can write your main function here, and perform the Huffman encoding
// in this file.

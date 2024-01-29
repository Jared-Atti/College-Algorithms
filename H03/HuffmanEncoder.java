import java.util.ArrayList;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.IOException;

/** Class HuffmanEncoder: You can include a main method and implement your encoding algorithm in this file.
	Use the get_tokens method to get an ArrayList of tokens.
**/
public class HuffmanEncoder {
	final static String alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

	public static ArrayList<String> process_word(String word) {
		ArrayList<String> frontlist = new ArrayList<String>();
		ArrayList<String> endlist = new ArrayList<String>();

		int i = 0;
		while(i < word.length() &&  alphabets.indexOf(word.charAt(i)) == -1) {
			frontlist.add(Character.toString(word.charAt(i)));
			i++;
		}
		int j = word.length()-1;
		while(j >= i && alphabets.indexOf(word.charAt(j)) == -1) {
			endlist.add(0, Character.toString(word.charAt(j)));
			j--;
		}
		String words = "";
		if(i <= j) {
			words = word.substring(i, j+1);
		}

		ArrayList<String> finalout = new ArrayList<String>();
		if(!frontlist.isEmpty()) {
			finalout.addAll(frontlist);
		}
		if(words != "") {
			finalout.add(words);
		}
		if(!endlist.isEmpty()) {
			finalout.addAll(endlist);
		}
		return finalout;
  }
	
	/** Takes a file name (inpfile) and returns an ArrayList of tokens.
		Throws an IOException if the file cannot be opened or read properly.
		Reads file in utf-8.
	**/
	public static ArrayList<String> get_tokens(String inpfile) throws IOException {
		ArrayList<String> tokens = new ArrayList<String>();
		BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(inpfile),"utf-8"));
		String str;
		while((str = reader.readLine()) != null) {
			str += "\n";
			for(String splitstr : str.split(" ")) {
				if(splitstr.equals("")) {
					tokens.add(" ");
					continue;
				}
				ArrayList<String> wordlist = process_word(splitstr);
				tokens.addAll(wordlist);
				if(!wordlist.get(wordlist.size()-1).equals("\n")) {
					tokens.add(" ");
				}
			}
		}
		reader.close();
		return tokens;
	}

}

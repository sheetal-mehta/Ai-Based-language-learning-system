"""
Based on the tips noted from the pronunciation code given by deutsch1, the below set of rules,
tips and suggestions are compiled and knit together in this below function.
Depending on the input sentence/word and associated phonemes, the tips are collated and 
printed for the user, so that they can refer this and prononuce the word/sentence properly.
This can be extended and refined with more specific cases from language or linguistic expert. 
"""
def pro_tip_user(sent,phones):
    sent = sent.split(" ")
    phones = phones.split(" ")
    tips = []
    for s in sent:
        if "ö" in s:
            tips.append("To speak ö first speak 'e'(German) & form your lips into an O form and keep the tongue in the same position as it was in 'e'.")
        
        if "ü" in s:
            tips.append("To speak ü first speak 'i'(German) without changing the tongue position and then form O lips. The underlip would be a bit out. ")

        if "ä" in s:
            tips.append("Prononuce ä same as 'e'.")
        
        if "chs" in s:
            tips.append("Note that 'chs' is prononuced as 'k' here.")
        
        if s[-2:]=="ig":
            tips.append("Note that 'ig' here in end is prononuced as 'ich'.")

        if s[0]=="s":
            tips.append("When a word starts with s then it the 's' is prononuced as 'z'.")

        if "eis" in s or "ies" in s or "eus" in s or "ues" in s or "aus" in s or "ous" in s or "aos" in s:
            tips.append("Whenever a dipthong is followed by 's' then 's' is prononuced as 'z'.")

        if "ah" in s or "eh" in s or "ih" in s or "oh" in s or "uh" in s:
            tips.append("When a vowel is followed by h then h is silent and vowel is elongated prononuced.")

        if s[-1]=="b" or s[-1]=="d" or s[-1]=="g":
            tips.append("Note that when words end with 'b','d','g' then they are pronounced 'p','t','k' respectively.")

    for p in phones:
        if "aː"in p or "eː" in p or "iː" in p or "oː" in p or "uː" in p:
            tips.append("a:,e:,i:,o:,u: - This is a long vowel, so stretch this whenever it appears.")
        
        if "a" in p or "ɛ" in p or "ɪ" in p or "ʊ" in p or "ɔ" in p:
            tips.append("a,ɛ, ɪ, ʊ,ɔ - These are short vowel phonemes, so do not stretch the vowel pronunciation.")
 
        if "ɐ" in p or "ɐ̯" in p:
            tips.append("For words with ɐ,ɐ̯ do not roll the r and prononuce the r as 'a'")
        
        if "ʃ" in p:
            tips.append("'ʃ' is prononuced as 'shh'. As if you are hushing. This is not elongated.")

    final_tips = list(set(tips))
    tips_str =" ".join(final_tips)

    return tips_str
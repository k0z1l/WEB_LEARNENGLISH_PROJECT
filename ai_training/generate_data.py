import json
import random

random.seed(42)

# ============================================================
# PHẦN 1: NGÂN HÀNG LỖI NGỮ PHÁP (80 MẪU ĐA DẠNG)
# ============================================================

grammar_errors = [
    # --- 1. Thì hiện tại đơn (Present Simple) ---
    {"wrong": "He go to school every day.", "correct": "He goes to school every day.", "error": "Chia sai động từ 'go' với chủ ngữ ngôi thứ 3 số ít 'He'.", "explain": "Với chủ ngữ ngôi thứ 3 số ít (He, She, It) ở thì hiện tại đơn, động từ phải thêm 's' hoặc 'es'."},
    {"wrong": "She don't like apples.", "correct": "She doesn't like apples.", "error": "Dùng sai trợ động từ 'don't' cho chủ ngữ ngôi thứ 3 số ít.", "explain": "Chủ ngữ số ít 'She' ở thì hiện tại đơn phủ định phải đi với 'doesn't'."},
    {"wrong": "I usually listens to music.", "correct": "I usually listen to music.", "error": "Chia sai động từ 'listens' với chủ ngữ 'I'.", "explain": "Với chủ ngữ 'I' ở thì hiện tại đơn, động từ giữ nguyên không thêm 's/es'."},
    {"wrong": "The sun rise in the east.", "correct": "The sun rises in the east.", "error": "Thiếu đuôi 's' cho động từ 'rise' với chủ ngữ 'The sun'.", "explain": "'The sun' là ngôi thứ 3 số ít, động từ phải thêm 's'."},
    {"wrong": "My mother cook dinner every evening.", "correct": "My mother cooks dinner every evening.", "error": "Thiếu đuôi 's' cho động từ 'cook'.", "explain": "'My mother' là ngôi thứ 3 số ít, động từ ở thì hiện tại đơn phải thêm 's'."},
    {"wrong": "He have a big house.", "correct": "He has a big house.", "error": "Chia sai động từ 'have' với chủ ngữ 'He'.", "explain": "Với chủ ngữ ngôi thứ 3 số ít, 'have' phải chuyển thành 'has'."},
    {"wrong": "Water freeze at 0 degrees.", "correct": "Water freezes at 0 degrees.", "error": "Thiếu đuôi 's' cho động từ 'freeze'.", "explain": "'Water' là danh từ không đếm được (ngôi thứ 3 số ít), động từ phải thêm 's'."},
    {"wrong": "She watch TV every night.", "correct": "She watches TV every night.", "error": "Thiếu đuôi 'es' cho động từ 'watch'.", "explain": "Động từ kết thúc bằng 'ch' phải thêm 'es' khi đi với chủ ngữ ngôi thứ 3 số ít."},
    {"wrong": "He play football on Sundays.", "correct": "He plays football on Sundays.", "error": "Thiếu đuôi 's' cho động từ 'play'.", "explain": "Chủ ngữ 'He' là ngôi thứ 3 số ít, thì hiện tại đơn phải thêm 's'."},
    {"wrong": "This machine work automatically.", "correct": "This machine works automatically.", "error": "Thiếu đuôi 's' cho động từ 'work'.", "explain": "'This machine' là ngôi thứ 3 số ít, động từ phải thêm 's'."},

    # --- 2. Thì quá khứ đơn (Past Simple) ---
    {"wrong": "I goed to the market yesterday.", "correct": "I went to the market yesterday.", "error": "Chia sai động từ bất quy tắc 'go' ở thì quá khứ đơn.", "explain": "'Go' là động từ bất quy tắc, quá khứ đơn là 'went' chứ không phải 'goed'."},
    {"wrong": "She buyed a new dress last week.", "correct": "She bought a new dress last week.", "error": "Chia sai động từ bất quy tắc 'buy'.", "explain": "'Buy' là động từ bất quy tắc, quá khứ đơn là 'bought'."},
    {"wrong": "Where you went last night?", "correct": "Where did you go last night?", "error": "Thiếu trợ động từ 'did' trong câu hỏi quá khứ đơn.", "explain": "Câu hỏi thì quá khứ đơn phải có 'did' và động từ chính ở dạng nguyên thể."},
    {"wrong": "He didn't went to school.", "correct": "He didn't go to school.", "error": "Dùng sai dạng động từ 'went' sau 'didn't'.", "explain": "Sau 'didn't', động từ phải ở dạng nguyên thể (go)."},
    {"wrong": "They was very happy.", "correct": "They were very happy.", "error": "Dùng sai 'was' cho chủ ngữ số nhiều 'They'.", "explain": "Chủ ngữ số nhiều 'They' phải đi với 'were'."},
    {"wrong": "He telled me the truth.", "correct": "He told me the truth.", "error": "Chia sai động từ bất quy tắc 'tell'.", "explain": "Quá khứ đơn của 'tell' là 'told', không phải 'telled'."},
    {"wrong": "She writed a long letter.", "correct": "She wrote a long letter.", "error": "Chia sai động từ bất quy tắc 'write'.", "explain": "Quá khứ đơn của 'write' là 'wrote', không phải 'writed'."},

    # --- 3. Thì hiện tại hoàn thành (Present Perfect) ---
    {"wrong": "I have been working here since 5 years.", "correct": "I have been working here for 5 years.", "error": "Dùng sai giới từ 'since' cho khoảng thời gian.", "explain": "'Since' dùng cho mốc thời gian, 'for' dùng cho khoảng thời gian."},
    {"wrong": "I have went to Paris yesterday.", "correct": "I went to Paris yesterday.", "error": "Dùng sai thì hiện tại hoàn thành với 'yesterday'.", "explain": "Khi có thời gian xác định trong quá khứ, phải dùng thì quá khứ đơn."},
    {"wrong": "She has already went home.", "correct": "She has already gone home.", "error": "Dùng sai quá khứ phân từ 'went' thay vì 'gone'.", "explain": "Thì hiện tại hoàn thành dùng 'has/have + V3'. V3 của 'go' là 'gone'."},
    {"wrong": "I have saw that movie before.", "correct": "I have seen that movie before.", "error": "Dùng sai quá khứ phân từ 'saw' thay vì 'seen'.", "explain": "V3 của 'see' là 'seen', không phải 'saw'."},
    {"wrong": "He have lived here for 10 years.", "correct": "He has lived here for 10 years.", "error": "Dùng sai 'have' cho chủ ngữ ngôi thứ 3 số ít.", "explain": "Chủ ngữ ngôi thứ 3 số ít phải dùng 'has'."},
    {"wrong": "We have knew each other for a long time.", "correct": "We have known each other for a long time.", "error": "Dùng sai quá khứ phân từ 'knew' thay vì 'known'.", "explain": "V3 của 'know' là 'known'."},

    # --- 4. Thì hiện tại tiếp diễn (Present Continuous) ---
    {"wrong": "She is cook dinner now.", "correct": "She is cooking dinner now.", "error": "Thiếu đuôi '-ing' cho động từ sau 'is'.", "explain": "Thì hiện tại tiếp diễn dùng 'is/am/are + V-ing'."},
    {"wrong": "They are study for the exam.", "correct": "They are studying for the exam.", "error": "Thiếu đuôi '-ing' cho động từ 'study'.", "explain": "Thì hiện tại tiếp diễn: 'are + studying'."},
    {"wrong": "I am work at the office now.", "correct": "I am working at the office now.", "error": "Thiếu đuôi '-ing' cho động từ 'work'.", "explain": "Thì hiện tại tiếp diễn: 'am + working'."},

    # --- 5. So sánh (Comparatives / Superlatives) ---
    {"wrong": "He is more taller than his brother.", "correct": "He is taller than his brother.", "error": "Thừa 'more' trong so sánh hơn của tính từ ngắn.", "explain": "Tính từ ngắn chỉ cần thêm '-er', không dùng 'more'."},
    {"wrong": "She is the most smartest student.", "correct": "She is the smartest student.", "error": "Thừa 'most' trong so sánh nhất của tính từ ngắn.", "explain": "Tính từ ngắn dùng đuôi '-est', không cần 'most'."},
    {"wrong": "This book is more better than that one.", "correct": "This book is better than that one.", "error": "Thừa 'more' trước 'better'.", "explain": "'Better' đã là dạng so sánh hơn của 'good'."},
    {"wrong": "He runs more fast than me.", "correct": "He runs faster than me.", "error": "Dùng 'more fast' thay vì 'faster'.", "explain": "'Fast' là trạng từ ngắn, so sánh hơn là 'faster'."},
    {"wrong": "This is the most worst day ever.", "correct": "This is the worst day ever.", "error": "Thừa 'most' trước 'worst'.", "explain": "'Worst' đã là dạng so sánh nhất của 'bad'."},

    # --- 6. Giới từ (Prepositions) ---
    {"wrong": "She is interested on reading books.", "correct": "She is interested in reading books.", "error": "Dùng sai giới từ 'on' sau 'interested'.", "explain": "Cụm từ cố định là 'interested in'."},
    {"wrong": "I am good in mathematics.", "correct": "I am good at mathematics.", "error": "Dùng sai giới từ 'in' sau 'good'.", "explain": "Cụm từ cố định là 'good at'."},
    {"wrong": "He depends of his parents.", "correct": "He depends on his parents.", "error": "Dùng sai giới từ 'of' sau 'depends'.", "explain": "Cụm từ cố định là 'depend on'."},
    {"wrong": "She married with a doctor.", "correct": "She married a doctor.", "error": "Thừa giới từ 'with' sau 'married'.", "explain": "'Marry' là ngoại động từ, đi trực tiếp với tân ngữ."},
    {"wrong": "I arrived to the airport.", "correct": "I arrived at the airport.", "error": "Dùng sai giới từ 'to' sau 'arrived'.", "explain": "Cụm từ cố định là 'arrive at'."},
    {"wrong": "We discussed about the problem.", "correct": "We discussed the problem.", "error": "Thừa giới từ 'about' sau 'discussed'.", "explain": "'Discuss' là ngoại động từ, không cần giới từ 'about'."},
    {"wrong": "He insisted for going alone.", "correct": "He insisted on going alone.", "error": "Dùng sai giới từ 'for' sau 'insisted'.", "explain": "Cụm từ cố định là 'insist on'."},
    {"wrong": "She apologized for arrive late.", "correct": "She apologized for arriving late.", "error": "Dùng sai dạng động từ sau giới từ 'for'.", "explain": "Sau giới từ, động từ phải ở dạng V-ing."},

    # --- 7. Động từ khuyết thiếu (Modal Verbs) ---
    {"wrong": "He can plays the guitar very well.", "correct": "He can play the guitar very well.", "error": "Chia sai động từ sau 'can'.", "explain": "Sau động từ khuyết thiếu, động từ luôn ở dạng nguyên thể."},
    {"wrong": "She must goes to the hospital.", "correct": "She must go to the hospital.", "error": "Chia sai động từ sau 'must'.", "explain": "Sau 'must', động từ luôn ở dạng nguyên thể."},
    {"wrong": "You should to study harder.", "correct": "You should study harder.", "error": "Thừa 'to' sau 'should'.", "explain": "Sau 'should', động từ đi trực tiếp ở dạng nguyên thể."},
    {"wrong": "They can to swim very fast.", "correct": "They can swim very fast.", "error": "Thừa 'to' sau 'can'.", "explain": "Sau 'can', động từ đi trực tiếp, không có 'to'."},
    {"wrong": "He must to finish the report.", "correct": "He must finish the report.", "error": "Thừa 'to' sau 'must'.", "explain": "Sau 'must', động từ đi trực tiếp ở dạng nguyên thể."},

    # --- 8. Mạo từ (Articles) ---
    {"wrong": "He is a honest man.", "correct": "He is an honest man.", "error": "Dùng sai mạo từ 'a' trước từ có chữ h câm.", "explain": "'Honest' bắt đầu bằng âm nguyên âm (h câm), nên phải dùng 'an'."},
    {"wrong": "She is an university student.", "correct": "She is a university student.", "error": "Dùng sai mạo từ 'an' trước từ bắt đầu bằng phụ âm.", "explain": "'University' bắt đầu bằng âm /juː/ (phụ âm), nên dùng 'a'."},
    {"wrong": "I want to buy a umbrella.", "correct": "I want to buy an umbrella.", "error": "Dùng sai mạo từ 'a' trước nguyên âm.", "explain": "'Umbrella' bắt đầu bằng nguyên âm /ʌ/, nên dùng 'an'."},
    {"wrong": "He is an European citizen.", "correct": "He is a European citizen.", "error": "Dùng sai mạo từ 'an' trước âm phụ âm.", "explain": "'European' bắt đầu bằng âm /jʊ/ (phụ âm), nên dùng 'a'."},

    # --- 9. Tính từ -ed / -ing ---
    {"wrong": "She was boring because the movie was bored.", "correct": "She was bored because the movie was boring.", "error": "Nhầm lẫn giữa tính từ đuôi -ed và -ing.", "explain": "-ed diễn tả cảm xúc của người, -ing diễn tả bản chất của sự vật."},
    {"wrong": "The lesson was very interested.", "correct": "The lesson was very interesting.", "error": "Dùng sai -ed cho sự vật.", "explain": "Sự vật dùng -ing (interesting), không phải -ed."},
    {"wrong": "I am very exciting about the trip.", "correct": "I am very excited about the trip.", "error": "Dùng sai -ing cho người.", "explain": "Con người diễn tả cảm xúc dùng -ed (excited)."},
    {"wrong": "The news is very surprised.", "correct": "The news is very surprising.", "error": "Dùng sai -ed cho sự vật.", "explain": "Sự vật gây ra cảm xúc dùng -ing (surprising)."},
    {"wrong": "He felt very embarrassing.", "correct": "He felt very embarrassed.", "error": "Dùng sai -ing cho người.", "explain": "Con người cảm thấy xấu hổ dùng 'embarrassed', không phải 'embarrassing'."},
    {"wrong": "The game was very tired.", "correct": "The game was very tiring.", "error": "Dùng sai -ed cho sự vật.", "explain": "Trò chơi gây mệt mỏi dùng 'tiring', không phải 'tired'."},

    # --- 10. Câu bị động (Passive Voice) ---
    {"wrong": "The cake was make by my mother.", "correct": "The cake was made by my mother.", "error": "Dùng sai dạng nguyên thể 'make' trong câu bị động.", "explain": "Câu bị động dùng 'was/were + V3'. V3 của 'make' là 'made'."},
    {"wrong": "English is speak all over the world.", "correct": "English is spoken all over the world.", "error": "Dùng sai dạng động từ trong câu bị động.", "explain": "Câu bị động: 'is + V3'. V3 của 'speak' là 'spoken'."},
    {"wrong": "The window was broke by the children.", "correct": "The window was broken by the children.", "error": "Dùng sai V2 'broke' thay vì V3 'broken'.", "explain": "Câu bị động dùng V3. V3 của 'break' là 'broken'."},

    # --- 11. Câu điều kiện (Conditionals) ---
    {"wrong": "If I will have money, I will buy a car.", "correct": "If I have money, I will buy a car.", "error": "Dùng 'will' trong mệnh đề if của câu điều kiện loại 1.", "explain": "Mệnh đề if trong câu điều kiện loại 1 dùng thì hiện tại đơn, không dùng 'will'."},
    {"wrong": "If I was you, I would study harder.", "correct": "If I were you, I would study harder.", "error": "Dùng 'was' thay vì 'were' trong câu điều kiện loại 2.", "explain": "Trong câu điều kiện loại 2, 'be' luôn chia thành 'were' cho tất cả các ngôi."},
    {"wrong": "If he would come, we would start.", "correct": "If he came, we would start.", "error": "Dùng 'would' trong mệnh đề if.", "explain": "Mệnh đề if trong câu điều kiện loại 2 dùng thì quá khứ đơn, không dùng 'would'."},

    # --- 12. Danh từ đếm được / không đếm được ---
    {"wrong": "The informations are useful.", "correct": "The information is useful.", "error": "Chia sai danh từ không đếm được 'information'.", "explain": "'Information' là danh từ không đếm được, không thêm 's' và đi với 'is'."},
    {"wrong": "I need some advices.", "correct": "I need some advice.", "error": "Thêm 's' cho danh từ không đếm được 'advice'.", "explain": "'Advice' là danh từ không đếm được, không có dạng số nhiều."},
    {"wrong": "She has many furnitures.", "correct": "She has much furniture.", "error": "Dùng sai 'many' và thêm 's' cho danh từ không đếm được.", "explain": "'Furniture' là danh từ không đếm được, dùng 'much' thay vì 'many'."},
    {"wrong": "Each students has a book.", "correct": "Each student has a book.", "error": "Dùng sai danh từ số nhiều sau 'Each'.", "explain": "'Each' luôn đi với danh từ số ít."},
    {"wrong": "The peoples in this room is nice.", "correct": "The people in this room are nice.", "error": "Sai dạng số nhiều của 'people' và chia sai động từ.", "explain": "'People' đã là số nhiều, không thêm 's', và đi với 'are'."},

    # --- 13. Cấu trúc đặc biệt ---
    {"wrong": "I look forward to see you.", "correct": "I look forward to seeing you.", "error": "Dùng sai dạng 'see' sau 'look forward to'.", "explain": "'Look forward to' yêu cầu V-ing theo sau."},
    {"wrong": "I suggest him to go home.", "correct": "I suggest that he go home.", "error": "Dùng sai cấu trúc 'suggest + to V'.", "explain": "'Suggest' đi với mệnh đề 'that + S + V nguyên thể'."},
    {"wrong": "He is enough tall to reach the shelf.", "correct": "He is tall enough to reach the shelf.", "error": "Đặt sai vị trí 'enough'.", "explain": "'Enough' đứng sau tính từ (tall enough)."},
    {"wrong": "Although it was raining, but we went out.", "correct": "Although it was raining, we went out.", "error": "Thừa 'but' khi đã có 'Although'.", "explain": "'Although' và 'but' không dùng cùng nhau."},
    {"wrong": "I am agree with you.", "correct": "I agree with you.", "error": "Thừa 'am' trước 'agree'.", "explain": "'Agree' là động từ thường, không cần 'am'."},
    {"wrong": "He gave to me a book.", "correct": "He gave me a book.", "error": "Thừa giới từ 'to' trong cấu trúc tân ngữ kép.", "explain": "Cấu trúc 'give + tân ngữ gián tiếp + tân ngữ trực tiếp' không cần 'to'."},
    {"wrong": "I didn't nothing.", "correct": "I didn't do anything.", "error": "Phủ định kép sai ngữ pháp.", "explain": "Trong tiếng Anh chuẩn, không dùng 2 từ phủ định liên tiếp."},

    # --- 14. Đại từ (Pronouns) ---
    {"wrong": "Me and him went to the park.", "correct": "He and I went to the park.", "error": "Dùng sai đại từ tân ngữ 'Me/him' làm chủ ngữ.", "explain": "Chủ ngữ phải dùng đại từ chủ ngữ (He and I), không dùng tân ngữ (Me and him)."},
    {"wrong": "Her and me are best friends.", "correct": "She and I are best friends.", "error": "Dùng sai đại từ tân ngữ làm chủ ngữ.", "explain": "Chủ ngữ phải dùng 'She and I'."},
    {"wrong": "The teacher gave the books to my friend and I.", "correct": "The teacher gave the books to my friend and me.", "error": "Dùng sai đại từ chủ ngữ 'I' làm tân ngữ sau giới từ.", "explain": "Sau giới từ 'to', phải dùng đại từ tân ngữ 'me'."},

    # --- 15. Trật tự từ (Word Order) ---
    {"wrong": "She speaks English very good.", "correct": "She speaks English very well.", "error": "Dùng tính từ 'good' thay vì trạng từ 'well'.", "explain": "Bổ nghĩa cho động từ 'speaks' phải dùng trạng từ 'well', không phải tính từ 'good'."},
    {"wrong": "I always am late for class.", "correct": "I am always late for class.", "error": "Đặt sai vị trí trạng từ tần suất 'always'.", "explain": "Trạng từ tần suất đứng sau động từ to be (am always)."},
    {"wrong": "He drives careful.", "correct": "He drives carefully.", "error": "Dùng tính từ 'careful' thay vì trạng từ 'carefully'.", "explain": "Bổ nghĩa cho động từ 'drives' phải dùng trạng từ 'carefully'."},

    # --- 16. Gerund vs Infinitive ---
    {"wrong": "I enjoy to play tennis.", "correct": "I enjoy playing tennis.", "error": "Dùng sai 'to play' sau 'enjoy'.", "explain": "'Enjoy' là động từ đòi hỏi V-ing theo sau, không dùng to V."},
    {"wrong": "She avoided to answer the question.", "correct": "She avoided answering the question.", "error": "Dùng sai 'to answer' sau 'avoided'.", "explain": "'Avoid' đòi hỏi V-ing theo sau."},
    {"wrong": "He decided going to the party.", "correct": "He decided to go to the party.", "error": "Dùng sai V-ing sau 'decided'.", "explain": "'Decide' đòi hỏi 'to V' theo sau."},
    {"wrong": "They finished to write the report.", "correct": "They finished writing the report.", "error": "Dùng sai 'to write' sau 'finished'.", "explain": "'Finish' đòi hỏi V-ing theo sau."},

    # --- 17. Câu tường thuật (Reported Speech) ---
    {"wrong": "He said that he is tired.", "correct": "He said that he was tired.", "error": "Không lùi thì trong câu tường thuật.", "explain": "Khi động từ tường thuật ở quá khứ (said), thì trong mệnh đề phải lùi 1 bậc (is -> was)."},
    {"wrong": "She told that she would come.", "correct": "She said that she would come.", "error": "Dùng 'told' mà không có tân ngữ.", "explain": "'Tell' bắt buộc phải có tân ngữ (told me/him/her). Không có tân ngữ thì dùng 'said'."},
]

# ============================================================
# PHẦN 2: NGÂN HÀNG CÂU ĐÚNG NGỮ PHÁP (40 MẪU)
# ============================================================

grammar_corrects = [
    {"text": "She always completes her assignments on time.", "explain": "Câu đúng: chủ ngữ số ít 'She' đi với động từ thêm 's' ở thì hiện tại đơn."},
    {"text": "I have been working here for 5 years.", "explain": "Câu đúng: dùng đúng 'for' với khoảng thời gian trong thì hiện tại hoàn thành tiếp diễn."},
    {"text": "If it rains tomorrow, we will cancel the trip.", "explain": "Câu điều kiện loại 1 đúng: mệnh đề if dùng thì hiện tại đơn, mệnh đề chính dùng 'will + V'."},
    {"text": "Water boils at 100 degrees Celsius.", "explain": "Câu đúng: diễn tả sự thật khoa học bằng thì hiện tại đơn."},
    {"text": "The book which you lent me is fascinating.", "explain": "Câu đúng: mệnh đề quan hệ với 'which' hoàn toàn chính xác."},
    {"text": "They have been studying English since 2020.", "explain": "Câu đúng: dùng 'since' với mốc thời gian cụ thể trong thì hiện tại hoàn thành tiếp diễn."},
    {"text": "He is taller than his brother.", "explain": "Câu đúng: so sánh hơn với tính từ ngắn dùng đuôi '-er' và 'than'."},
    {"text": "She can speak three languages fluently.", "explain": "Câu đúng: sau 'can', động từ 'speak' ở dạng nguyên thể."},
    {"text": "I have already finished my homework.", "explain": "Câu đúng: thì hiện tại hoàn thành với 'have + V3' và trạng từ 'already'."},
    {"text": "The children are playing in the garden.", "explain": "Câu đúng: thì hiện tại tiếp diễn, chủ ngữ số nhiều 'children' đi với 'are'."},
    {"text": "Neither the students nor the teacher was absent.", "explain": "Câu đúng: với 'neither...nor', động từ chia theo chủ ngữ gần nhất."},
    {"text": "He would rather stay at home than go out.", "explain": "Câu đúng: cấu trúc 'would rather + V + than + V' ở dạng nguyên thể."},
    {"text": "By the time we arrived, the movie had already started.", "explain": "Câu đúng: thì quá khứ hoàn thành diễn tả hành động xảy ra trước."},
    {"text": "She is one of the most talented singers in the world.", "explain": "Câu đúng: so sánh nhất với tính từ dài dùng 'most + adj'."},
    {"text": "I wish I were taller.", "explain": "Câu đúng: cấu trúc 'wish + quá khứ giả định', dùng 'were' cho tất cả các ngôi."},
    {"text": "Not only does he sing well, but he also plays the piano.", "explain": "Câu đúng: cấu trúc đảo ngữ 'Not only + trợ động từ + S + V'."},
    {"text": "The more you practice, the better you become.", "explain": "Câu đúng: cấu trúc so sánh kép 'The more...the better'."},
    {"text": "Had I known about the meeting, I would have attended.", "explain": "Câu đúng: câu điều kiện loại 3 dạng đảo ngữ."},
    {"text": "Despite being tired, she continued working.", "explain": "Câu đúng: 'despite + V-ing' diễn tả sự tương phản."},
    {"text": "It is essential that he be present at the meeting.", "explain": "Câu đúng: cấu trúc giả định (subjunctive mood)."},
    {"text": "The project will have been completed by next month.", "explain": "Câu đúng: thì tương lai hoàn thành bị động."},
    {"text": "He apologized for being late.", "explain": "Câu đúng: 'apologize for + V-ing' hoàn toàn chính xác."},
    {"text": "She is used to waking up early.", "explain": "Câu đúng: 'be used to + V-ing' nghĩa là quen với việc gì."},
    {"text": "The teacher made the students do the exercise.", "explain": "Câu đúng: cấu trúc 'make + O + V nguyên thể'."},
    {"text": "I would have gone if you had told me.", "explain": "Câu đúng: câu điều kiện loại 3 hoàn toàn chính xác."},
    {"text": "He suggested that we take a break.", "explain": "Câu đúng: 'suggest that + S + V nguyên thể' (subjunctive)."},
    {"text": "No sooner had he arrived than it started raining.", "explain": "Câu đúng: cấu trúc đảo ngữ 'No sooner...than'."},
    {"text": "She asked me whether I had finished the work.", "explain": "Câu đúng: câu tường thuật dạng câu hỏi với 'whether'."},
    {"text": "Having finished the report, she went home.", "explain": "Câu đúng: phân từ hoàn thành (Having + V3) diễn tả hành động xảy ra trước."},
    {"text": "Were it not for your help, I would have failed.", "explain": "Câu đúng: câu điều kiện loại 3 dạng đảo ngữ với 'Were it not for'."},
    {"text": "He runs faster than anyone else in the class.", "explain": "Câu đúng: so sánh hơn với trạng từ ngắn 'faster'."},
    {"text": "The woman whose car was stolen called the police.", "explain": "Câu đúng: mệnh đề quan hệ sở hữu với 'whose'."},
    {"text": "I have never seen such a beautiful sunset.", "explain": "Câu đúng: 'such a + adj + N' hoàn toàn chính xác."},
    {"text": "You had better not be late again.", "explain": "Câu đúng: 'had better not + V nguyên thể' để khuyên ai không nên làm gì."},
    {"text": "Hardly had she opened the door when the phone rang.", "explain": "Câu đúng: cấu trúc đảo ngữ 'Hardly...when'."},
    {"text": "He is believed to be the best candidate.", "explain": "Câu đúng: cấu trúc bị động với động từ tường thuật 'believe'."},
    {"text": "She insisted on paying for the dinner.", "explain": "Câu đúng: 'insist on + V-ing' hoàn toàn chính xác."},
    {"text": "Not until I got home did I realize I had lost my keys.", "explain": "Câu đúng: cấu trúc đảo ngữ 'Not until...did I'."},
    {"text": "The sooner you finish, the sooner you can leave.", "explain": "Câu đúng: cấu trúc so sánh kép 'The sooner...the sooner'."},
    {"text": "All the documents need to be signed before Friday.", "explain": "Câu đúng: cấu trúc bị động với 'need to be + V3'."},
]

# ============================================================
# PHẦN 3: NGÂN HÀNG TỪ VỰNG (25 CHỦ ĐỀ x 5 TỪ)
# ============================================================

vocab_database = {
    "Office": [
        {"en": "colleague", "vi": "đồng nghiệp", "pos": "N", "pron": "/ˈkɒliːɡ/", "ex_en": "I respect my colleagues.", "ex_vi": "Tôi tôn trọng các đồng nghiệp."},
        {"en": "deadline", "vi": "hạn chót", "pos": "N", "pron": "/ˈdedlaɪn/", "ex_en": "We must meet the deadline.", "ex_vi": "Chúng ta phải hoàn thành trước hạn chót."},
        {"en": "agenda", "vi": "chương trình nghị sự", "pos": "N", "pron": "/əˈdʒendə/", "ex_en": "Let me check the agenda.", "ex_vi": "Để tôi kiểm tra chương trình nghị sự."},
        {"en": "overtime", "vi": "làm thêm giờ", "pos": "N", "pron": "/ˈəʊvətaɪm/", "ex_en": "I worked overtime yesterday.", "ex_vi": "Tôi đã làm thêm giờ hôm qua."},
        {"en": "supervisor", "vi": "người giám sát", "pos": "N", "pron": "/ˈsuːpəvaɪzər/", "ex_en": "My supervisor approved the plan.", "ex_vi": "Giám sát của tôi đã phê duyệt kế hoạch."},
    ],
    "Business": [
        {"en": "negotiate", "vi": "đàm phán", "pos": "V", "pron": "/nɪˈɡəʊʃieɪt/", "ex_en": "We need to negotiate the contract.", "ex_vi": "Chúng ta cần đàm phán hợp đồng."},
        {"en": "revenue", "vi": "doanh thu", "pos": "N", "pron": "/ˈrevənjuː/", "ex_en": "Revenue increased by 20%.", "ex_vi": "Doanh thu tăng 20%."},
        {"en": "profitable", "vi": "có lợi nhuận", "pos": "Adj", "pron": "/ˈprɒfɪtəbl/", "ex_en": "The business is profitable.", "ex_vi": "Doanh nghiệp có lợi nhuận."},
        {"en": "invest", "vi": "đầu tư", "pos": "V", "pron": "/ɪnˈvest/", "ex_en": "They invest in technology.", "ex_vi": "Họ đầu tư vào công nghệ."},
        {"en": "shareholder", "vi": "cổ đông", "pos": "N", "pron": "/ˈʃeəhəʊldər/", "ex_en": "Shareholders approved the plan.", "ex_vi": "Các cổ đông đã phê duyệt kế hoạch."},
    ],
    "Technology": [
        {"en": "algorithm", "vi": "thuật toán", "pos": "N", "pron": "/ˈælɡərɪðəm/", "ex_en": "This algorithm is efficient.", "ex_vi": "Thuật toán này hiệu quả."},
        {"en": "database", "vi": "cơ sở dữ liệu", "pos": "N", "pron": "/ˈdeɪtəbeɪs/", "ex_en": "The database stores user data.", "ex_vi": "Cơ sở dữ liệu lưu trữ dữ liệu người dùng."},
        {"en": "encrypt", "vi": "mã hóa", "pos": "V", "pron": "/ɪnˈkrɪpt/", "ex_en": "We encrypt sensitive data.", "ex_vi": "Chúng tôi mã hóa dữ liệu nhạy cảm."},
        {"en": "bandwidth", "vi": "băng thông", "pos": "N", "pron": "/ˈbændwɪdθ/", "ex_en": "We need more bandwidth.", "ex_vi": "Chúng ta cần thêm băng thông."},
        {"en": "compatible", "vi": "tương thích", "pos": "Adj", "pron": "/kəmˈpætəbl/", "ex_en": "These devices are compatible.", "ex_vi": "Các thiết bị này tương thích."},
    ],
    "Health": [
        {"en": "symptom", "vi": "triệu chứng", "pos": "N", "pron": "/ˈsɪmptəm/", "ex_en": "What are the symptoms?", "ex_vi": "Các triệu chứng là gì?"},
        {"en": "prescription", "vi": "đơn thuốc", "pos": "N", "pron": "/prɪˈskrɪpʃn/", "ex_en": "The doctor wrote a prescription.", "ex_vi": "Bác sĩ đã viết đơn thuốc."},
        {"en": "diagnose", "vi": "chẩn đoán", "pos": "V", "pron": "/ˈdaɪəɡnəʊz/", "ex_en": "The doctor diagnosed the illness.", "ex_vi": "Bác sĩ đã chẩn đoán bệnh."},
        {"en": "immune", "vi": "miễn dịch", "pos": "Adj", "pron": "/ɪˈmjuːn/", "ex_en": "Exercise boosts the immune system.", "ex_vi": "Tập thể dục tăng cường hệ miễn dịch."},
        {"en": "therapy", "vi": "liệu pháp", "pos": "N", "pron": "/ˈθerəpi/", "ex_en": "She needs physical therapy.", "ex_vi": "Cô ấy cần liệu pháp vật lý."},
    ],
    "Education": [
        {"en": "curriculum", "vi": "chương trình giảng dạy", "pos": "N", "pron": "/kəˈrɪkjələm/", "ex_en": "The curriculum was updated.", "ex_vi": "Chương trình giảng dạy đã được cập nhật."},
        {"en": "scholarship", "vi": "học bổng", "pos": "N", "pron": "/ˈskɒləʃɪp/", "ex_en": "She won a full scholarship.", "ex_vi": "Cô ấy đã giành được học bổng toàn phần."},
        {"en": "lecture", "vi": "bài giảng", "pos": "N", "pron": "/ˈlektʃər/", "ex_en": "The lecture was informative.", "ex_vi": "Bài giảng rất nhiều thông tin."},
        {"en": "enrollment", "vi": "sự ghi danh", "pos": "N", "pron": "/ɪnˈrəʊlmənt/", "ex_en": "Enrollment starts next month.", "ex_vi": "Việc ghi danh bắt đầu vào tháng sau."},
        {"en": "evaluate", "vi": "đánh giá", "pos": "V", "pron": "/ɪˈvæljueɪt/", "ex_en": "We need to evaluate the results.", "ex_vi": "Chúng ta cần đánh giá kết quả."},
    ],
    "Travel": [
        {"en": "itinerary", "vi": "lịch trình", "pos": "N", "pron": "/aɪˈtɪnərəri/", "ex_en": "Check the travel itinerary.", "ex_vi": "Kiểm tra lịch trình du lịch."},
        {"en": "accommodation", "vi": "chỗ ở", "pos": "N", "pron": "/əˌkɒməˈdeɪʃn/", "ex_en": "The accommodation was comfortable.", "ex_vi": "Chỗ ở rất thoải mái."},
        {"en": "departure", "vi": "sự khởi hành", "pos": "N", "pron": "/dɪˈpɑːtʃər/", "ex_en": "The departure time is 8 AM.", "ex_vi": "Giờ khởi hành là 8 giờ sáng."},
        {"en": "destination", "vi": "điểm đến", "pos": "N", "pron": "/ˌdestɪˈneɪʃn/", "ex_en": "Paris is a popular destination.", "ex_vi": "Paris là một điểm đến phổ biến."},
        {"en": "luggage", "vi": "hành lý", "pos": "N", "pron": "/ˈlʌɡɪdʒ/", "ex_en": "Don't forget your luggage.", "ex_vi": "Đừng quên hành lý của bạn."},
    ],
    "Environment": [
        {"en": "pollution", "vi": "ô nhiễm", "pos": "N", "pron": "/pəˈluːʃn/", "ex_en": "Air pollution is a serious problem.", "ex_vi": "Ô nhiễm không khí là vấn đề nghiêm trọng."},
        {"en": "sustainable", "vi": "bền vững", "pos": "Adj", "pron": "/səˈsteɪnəbl/", "ex_en": "We need sustainable solutions.", "ex_vi": "Chúng ta cần các giải pháp bền vững."},
        {"en": "renewable", "vi": "tái tạo", "pos": "Adj", "pron": "/rɪˈnjuːəbl/", "ex_en": "Solar energy is renewable.", "ex_vi": "Năng lượng mặt trời là tái tạo."},
        {"en": "ecosystem", "vi": "hệ sinh thái", "pos": "N", "pron": "/ˈiːkəʊsɪstəm/", "ex_en": "The ecosystem is fragile.", "ex_vi": "Hệ sinh thái rất mong manh."},
        {"en": "deforestation", "vi": "nạn phá rừng", "pos": "N", "pron": "/diːˌfɒrɪˈsteɪʃn/", "ex_en": "Deforestation threatens wildlife.", "ex_vi": "Nạn phá rừng đe dọa động vật hoang dã."},
    ],
    "Finance": [
        {"en": "mortgage", "vi": "thế chấp", "pos": "N", "pron": "/ˈmɔːɡɪdʒ/", "ex_en": "They took out a mortgage.", "ex_vi": "Họ đã vay thế chấp."},
        {"en": "inflation", "vi": "lạm phát", "pos": "N", "pron": "/ɪnˈfleɪʃn/", "ex_en": "Inflation is rising rapidly.", "ex_vi": "Lạm phát đang tăng nhanh."},
        {"en": "dividend", "vi": "cổ tức", "pos": "N", "pron": "/ˈdɪvɪdend/", "ex_en": "The company paid dividends.", "ex_vi": "Công ty đã trả cổ tức."},
        {"en": "audit", "vi": "kiểm toán", "pos": "N", "pron": "/ˈɔːdɪt/", "ex_en": "The audit revealed some issues.", "ex_vi": "Cuộc kiểm toán phát hiện một số vấn đề."},
        {"en": "expenditure", "vi": "chi tiêu", "pos": "N", "pron": "/ɪkˈspendɪtʃər/", "ex_en": "We must reduce expenditure.", "ex_vi": "Chúng ta phải giảm chi tiêu."},
    ],
    "Transportation": [
        {"en": "commute", "vi": "đi lại hàng ngày", "pos": "V", "pron": "/kəˈmjuːt/", "ex_en": "I commute to work by train.", "ex_vi": "Tôi đi làm bằng tàu hàng ngày."},
        {"en": "congestion", "vi": "tắc nghẽn", "pos": "N", "pron": "/kənˈdʒestʃən/", "ex_en": "Traffic congestion is terrible.", "ex_vi": "Tắc nghẽn giao thông rất kinh khủng."},
        {"en": "pedestrian", "vi": "người đi bộ", "pos": "N", "pron": "/pəˈdestriən/", "ex_en": "Pedestrians should use crosswalks.", "ex_vi": "Người đi bộ nên sử dụng vạch kẻ đường."},
        {"en": "vehicle", "vi": "phương tiện", "pos": "N", "pron": "/ˈviːəkl/", "ex_en": "Electric vehicles are popular.", "ex_vi": "Xe điện đang phổ biến."},
        {"en": "intersection", "vi": "ngã tư", "pos": "N", "pron": "/ˌɪntəˈsekʃn/", "ex_en": "Turn left at the intersection.", "ex_vi": "Rẽ trái ở ngã tư."},
    ],
    "Law": [
        {"en": "verdict", "vi": "phán quyết", "pos": "N", "pron": "/ˈvɜːdɪkt/", "ex_en": "The jury delivered a verdict.", "ex_vi": "Bồi thẩm đoàn đã đưa ra phán quyết."},
        {"en": "legislation", "vi": "pháp luật", "pos": "N", "pron": "/ˌledʒɪˈsleɪʃn/", "ex_en": "New legislation was introduced.", "ex_vi": "Luật mới đã được ban hành."},
        {"en": "prosecute", "vi": "truy tố", "pos": "V", "pron": "/ˈprɒsɪkjuːt/", "ex_en": "They decided to prosecute.", "ex_vi": "Họ quyết định truy tố."},
        {"en": "testimony", "vi": "lời khai", "pos": "N", "pron": "/ˈtestɪməni/", "ex_en": "Her testimony was crucial.", "ex_vi": "Lời khai của cô ấy rất quan trọng."},
        {"en": "defendant", "vi": "bị cáo", "pos": "N", "pron": "/dɪˈfendənt/", "ex_en": "The defendant pleaded not guilty.", "ex_vi": "Bị cáo không nhận tội."},
    ],
    "Marketing": [
        {"en": "campaign", "vi": "chiến dịch", "pos": "N", "pron": "/kæmˈpeɪn/", "ex_en": "The marketing campaign was successful.", "ex_vi": "Chiến dịch tiếp thị đã thành công."},
        {"en": "brand", "vi": "thương hiệu", "pos": "N", "pron": "/brænd/", "ex_en": "This brand is very popular.", "ex_vi": "Thương hiệu này rất phổ biến."},
        {"en": "target", "vi": "mục tiêu", "pos": "N", "pron": "/ˈtɑːɡɪt/", "ex_en": "We met our sales target.", "ex_vi": "Chúng tôi đã đạt mục tiêu doanh số."},
        {"en": "strategy", "vi": "chiến lược", "pos": "N", "pron": "/ˈstrætədʒi/", "ex_en": "We need a new strategy.", "ex_vi": "Chúng ta cần một chiến lược mới."},
        {"en": "consumer", "vi": "người tiêu dùng", "pos": "N", "pron": "/kənˈsjuːmər/", "ex_en": "Consumer demand is increasing.", "ex_vi": "Nhu cầu người tiêu dùng đang tăng."},
    ],
    "Cybersecurity": [
        {"en": "firewall", "vi": "tường lửa", "pos": "N", "pron": "/ˈfaɪəwɔːl/", "ex_en": "The firewall blocked the attack.", "ex_vi": "Tường lửa đã chặn cuộc tấn công."},
        {"en": "phishing", "vi": "lừa đảo trực tuyến", "pos": "N", "pron": "/ˈfɪʃɪŋ/", "ex_en": "Beware of phishing emails.", "ex_vi": "Hãy cẩn thận với email lừa đảo."},
        {"en": "vulnerability", "vi": "lỗ hổng bảo mật", "pos": "N", "pron": "/ˌvʌlnərəˈbɪləti/", "ex_en": "They found a critical vulnerability.", "ex_vi": "Họ đã tìm thấy một lỗ hổng nghiêm trọng."},
        {"en": "malware", "vi": "phần mềm độc hại", "pos": "N", "pron": "/ˈmælweər/", "ex_en": "The system was infected with malware.", "ex_vi": "Hệ thống bị nhiễm phần mềm độc hại."},
        {"en": "authentication", "vi": "xác thực", "pos": "N", "pron": "/ɔːˌθentɪˈkeɪʃn/", "ex_en": "Two-factor authentication is required.", "ex_vi": "Yêu cầu xác thực hai yếu tố."},
    ],
    "Food": [
        {"en": "cuisine", "vi": "ẩm thực", "pos": "N", "pron": "/kwɪˈziːn/", "ex_en": "Vietnamese cuisine is delicious.", "ex_vi": "Ẩm thực Việt Nam rất ngon."},
        {"en": "ingredient", "vi": "nguyên liệu", "pos": "N", "pron": "/ɪnˈɡriːdiənt/", "ex_en": "We need fresh ingredients.", "ex_vi": "Chúng ta cần nguyên liệu tươi."},
        {"en": "appetizer", "vi": "món khai vị", "pos": "N", "pron": "/ˈæpɪtaɪzər/", "ex_en": "The appetizer was excellent.", "ex_vi": "Món khai vị rất tuyệt vời."},
        {"en": "beverage", "vi": "đồ uống", "pos": "N", "pron": "/ˈbevərɪdʒ/", "ex_en": "Would you like a beverage?", "ex_vi": "Bạn có muốn dùng đồ uống không?"},
        {"en": "nutritious", "vi": "bổ dưỡng", "pos": "Adj", "pron": "/njuːˈtrɪʃəs/", "ex_en": "This meal is very nutritious.", "ex_vi": "Bữa ăn này rất bổ dưỡng."},
    ],
    "Sports": [
        {"en": "championship", "vi": "giải vô địch", "pos": "N", "pron": "/ˈtʃæmpiənʃɪp/", "ex_en": "They won the championship.", "ex_vi": "Họ đã giành chức vô địch."},
        {"en": "tournament", "vi": "giải đấu", "pos": "N", "pron": "/ˈtʊənəmənt/", "ex_en": "The tournament starts tomorrow.", "ex_vi": "Giải đấu bắt đầu vào ngày mai."},
        {"en": "referee", "vi": "trọng tài", "pos": "N", "pron": "/ˌrefəˈriː/", "ex_en": "The referee made a fair decision.", "ex_vi": "Trọng tài đã đưa ra quyết định công bằng."},
        {"en": "endurance", "vi": "sức bền", "pos": "N", "pron": "/ɪnˈdjʊərəns/", "ex_en": "Running builds endurance.", "ex_vi": "Chạy bộ xây dựng sức bền."},
        {"en": "opponent", "vi": "đối thủ", "pos": "N", "pron": "/əˈpəʊnənt/", "ex_en": "He defeated his opponent.", "ex_vi": "Anh ấy đã đánh bại đối thủ."},
    ],
    "Entertainment": [
        {"en": "premiere", "vi": "buổi công chiếu", "pos": "N", "pron": "/prɪˈmɪər/", "ex_en": "The movie premiere was spectacular.", "ex_vi": "Buổi công chiếu phim rất ngoạn mục."},
        {"en": "audience", "vi": "khán giả", "pos": "N", "pron": "/ˈɔːdiəns/", "ex_en": "The audience loved the show.", "ex_vi": "Khán giả yêu thích buổi biểu diễn."},
        {"en": "rehearsal", "vi": "buổi tập dượt", "pos": "N", "pron": "/rɪˈhɜːsl/", "ex_en": "The rehearsal went well.", "ex_vi": "Buổi tập dượt diễn ra tốt đẹp."},
        {"en": "celebrity", "vi": "người nổi tiếng", "pos": "N", "pron": "/sɪˈlebrəti/", "ex_en": "She became a celebrity overnight.", "ex_vi": "Cô ấy trở nên nổi tiếng chỉ sau một đêm."},
        {"en": "broadcast", "vi": "phát sóng", "pos": "V", "pron": "/ˈbrɔːdkɑːst/", "ex_en": "The event was broadcast live.", "ex_vi": "Sự kiện được phát sóng trực tiếp."},
    ],
    "Real Estate": [
        {"en": "tenant", "vi": "người thuê nhà", "pos": "N", "pron": "/ˈtenənt/", "ex_en": "The tenant signed a lease.", "ex_vi": "Người thuê nhà đã ký hợp đồng thuê."},
        {"en": "landlord", "vi": "chủ nhà", "pos": "N", "pron": "/ˈlændlɔːd/", "ex_en": "The landlord raised the rent.", "ex_vi": "Chủ nhà đã tăng tiền thuê."},
        {"en": "renovation", "vi": "sự cải tạo", "pos": "N", "pron": "/ˌrenəˈveɪʃn/", "ex_en": "The renovation took six months.", "ex_vi": "Việc cải tạo mất sáu tháng."},
        {"en": "property", "vi": "bất động sản", "pos": "N", "pron": "/ˈprɒpəti/", "ex_en": "Property prices are rising.", "ex_vi": "Giá bất động sản đang tăng."},
        {"en": "lease", "vi": "hợp đồng thuê", "pos": "N", "pron": "/liːs/", "ex_en": "The lease expires next year.", "ex_vi": "Hợp đồng thuê hết hạn vào năm sau."},
    ],
    "Human Resources": [
        {"en": "recruitment", "vi": "tuyển dụng", "pos": "N", "pron": "/rɪˈkruːtmənt/", "ex_en": "Recruitment is ongoing.", "ex_vi": "Việc tuyển dụng đang diễn ra."},
        {"en": "probation", "vi": "thời gian thử việc", "pos": "N", "pron": "/prəˈbeɪʃn/", "ex_en": "He is still on probation.", "ex_vi": "Anh ấy vẫn đang trong thời gian thử việc."},
        {"en": "resignation", "vi": "sự từ chức", "pos": "N", "pron": "/ˌrezɪɡˈneɪʃn/", "ex_en": "She submitted her resignation.", "ex_vi": "Cô ấy đã nộp đơn từ chức."},
        {"en": "appraisal", "vi": "đánh giá hiệu suất", "pos": "N", "pron": "/əˈpreɪzl/", "ex_en": "The annual appraisal is next week.", "ex_vi": "Đánh giá thường niên vào tuần sau."},
        {"en": "compensation", "vi": "bồi thường, lương thưởng", "pos": "N", "pron": "/ˌkɒmpenˈseɪʃn/", "ex_en": "The compensation package is attractive.", "ex_vi": "Gói lương thưởng rất hấp dẫn."},
    ],
    "Manufacturing": [
        {"en": "assembly", "vi": "lắp ráp", "pos": "N", "pron": "/əˈsembli/", "ex_en": "The assembly line is automated.", "ex_vi": "Dây chuyền lắp ráp được tự động hóa."},
        {"en": "defect", "vi": "lỗi, khuyết điểm", "pos": "N", "pron": "/ˈdiːfekt/", "ex_en": "The product has a defect.", "ex_vi": "Sản phẩm có lỗi."},
        {"en": "warehouse", "vi": "nhà kho", "pos": "N", "pron": "/ˈweəhaʊs/", "ex_en": "The warehouse is full.", "ex_vi": "Nhà kho đã đầy."},
        {"en": "inventory", "vi": "hàng tồn kho", "pos": "N", "pron": "/ˈɪnvəntri/", "ex_en": "We need to check the inventory.", "ex_vi": "Chúng ta cần kiểm tra hàng tồn kho."},
        {"en": "efficiency", "vi": "hiệu suất", "pos": "N", "pron": "/ɪˈfɪʃnsi/", "ex_en": "We improved production efficiency.", "ex_vi": "Chúng tôi đã cải thiện hiệu suất sản xuất."},
    ],
    "Logistics": [
        {"en": "shipment", "vi": "lô hàng", "pos": "N", "pron": "/ˈʃɪpmənt/", "ex_en": "The shipment arrived on time.", "ex_vi": "Lô hàng đã đến đúng hẹn."},
        {"en": "freight", "vi": "hàng hóa vận chuyển", "pos": "N", "pron": "/freɪt/", "ex_en": "Freight costs have increased.", "ex_vi": "Chi phí vận chuyển hàng hóa đã tăng."},
        {"en": "dispatch", "vi": "gửi đi", "pos": "V", "pron": "/dɪˈspætʃ/", "ex_en": "We will dispatch the order today.", "ex_vi": "Chúng tôi sẽ gửi đơn hàng hôm nay."},
        {"en": "customs", "vi": "hải quan", "pos": "N", "pron": "/ˈkʌstəmz/", "ex_en": "The goods cleared customs.", "ex_vi": "Hàng hóa đã thông quan."},
        {"en": "tracking", "vi": "theo dõi", "pos": "N", "pron": "/ˈtrækɪŋ/", "ex_en": "Check the tracking number.", "ex_vi": "Kiểm tra mã theo dõi."},
    ],
    "Media": [
        {"en": "journalism", "vi": "báo chí", "pos": "N", "pron": "/ˈdʒɜːnəlɪzəm/", "ex_en": "Journalism requires integrity.", "ex_vi": "Báo chí đòi hỏi sự chính trực."},
        {"en": "headline", "vi": "tiêu đề", "pos": "N", "pron": "/ˈhedlaɪn/", "ex_en": "The headline attracted attention.", "ex_vi": "Tiêu đề thu hút sự chú ý."},
        {"en": "editorial", "vi": "bài xã luận", "pos": "N", "pron": "/ˌedɪˈtɔːriəl/", "ex_en": "She wrote an editorial.", "ex_vi": "Cô ấy đã viết một bài xã luận."},
        {"en": "correspondent", "vi": "phóng viên", "pos": "N", "pron": "/ˌkɒrɪˈspɒndənt/", "ex_en": "The correspondent reported from London.", "ex_vi": "Phóng viên tường thuật từ London."},
        {"en": "circulation", "vi": "số lượng phát hành", "pos": "N", "pron": "/ˌsɜːkjəˈleɪʃn/", "ex_en": "The newspaper has a large circulation.", "ex_vi": "Tờ báo có số lượng phát hành lớn."},
    ],
    "Agriculture": [
        {"en": "harvest", "vi": "thu hoạch", "pos": "V", "pron": "/ˈhɑːvɪst/", "ex_en": "Farmers harvest rice in autumn.", "ex_vi": "Nông dân thu hoạch lúa vào mùa thu."},
        {"en": "fertilizer", "vi": "phân bón", "pos": "N", "pron": "/ˈfɜːtəlaɪzər/", "ex_en": "Organic fertilizer is preferred.", "ex_vi": "Phân bón hữu cơ được ưa chuộng."},
        {"en": "irrigation", "vi": "tưới tiêu", "pos": "N", "pron": "/ˌɪrɪˈɡeɪʃn/", "ex_en": "Irrigation is vital for farming.", "ex_vi": "Tưới tiêu rất quan trọng cho nông nghiệp."},
        {"en": "cultivate", "vi": "trồng trọt", "pos": "V", "pron": "/ˈkʌltɪveɪt/", "ex_en": "They cultivate organic vegetables.", "ex_vi": "Họ trồng rau hữu cơ."},
        {"en": "livestock", "vi": "gia súc", "pos": "N", "pron": "/ˈlaɪvstɒk/", "ex_en": "Livestock farming is common here.", "ex_vi": "Chăn nuôi gia súc phổ biến ở đây."},
    ],
    "Energy": [
        {"en": "fossil fuel", "vi": "nhiên liệu hóa thạch", "pos": "N", "pron": "/ˌfɒsl ˈfjuːəl/", "ex_en": "We must reduce fossil fuel use.", "ex_vi": "Chúng ta phải giảm sử dụng nhiên liệu hóa thạch."},
        {"en": "solar panel", "vi": "tấm pin mặt trời", "pos": "N", "pron": "/ˌsəʊlə ˈpænl/", "ex_en": "Solar panels generate electricity.", "ex_vi": "Tấm pin mặt trời tạo ra điện."},
        {"en": "turbine", "vi": "tua-bin", "pos": "N", "pron": "/ˈtɜːbaɪn/", "ex_en": "Wind turbines are installed offshore.", "ex_vi": "Tua-bin gió được lắp đặt ngoài khơi."},
        {"en": "emission", "vi": "khí thải", "pos": "N", "pron": "/ɪˈmɪʃn/", "ex_en": "Carbon emissions must be reduced.", "ex_vi": "Khí thải carbon phải được giảm."},
        {"en": "conservation", "vi": "bảo tồn", "pos": "N", "pron": "/ˌkɒnsəˈveɪʃn/", "ex_en": "Energy conservation is important.", "ex_vi": "Bảo tồn năng lượng rất quan trọng."},
    ],
    "Fashion": [
        {"en": "couture", "vi": "thời trang cao cấp", "pos": "N", "pron": "/kuːˈtjʊər/", "ex_en": "She designs haute couture.", "ex_vi": "Cô ấy thiết kế thời trang cao cấp."},
        {"en": "textile", "vi": "vải dệt", "pos": "N", "pron": "/ˈtekstaɪl/", "ex_en": "The textile industry is growing.", "ex_vi": "Ngành dệt may đang phát triển."},
        {"en": "accessory", "vi": "phụ kiện", "pos": "N", "pron": "/əkˈsesəri/", "ex_en": "She bought some accessories.", "ex_vi": "Cô ấy đã mua một số phụ kiện."},
        {"en": "garment", "vi": "trang phục", "pos": "N", "pron": "/ˈɡɑːmənt/", "ex_en": "This garment is handmade.", "ex_vi": "Trang phục này được làm thủ công."},
        {"en": "runway", "vi": "sàn diễn", "pos": "N", "pron": "/ˈrʌnweɪ/", "ex_en": "Models walked the runway.", "ex_vi": "Các người mẫu trình diễn trên sàn diễn."},
    ],
    "Psychology": [
        {"en": "anxiety", "vi": "lo âu", "pos": "N", "pron": "/æŋˈzaɪəti/", "ex_en": "She suffers from anxiety.", "ex_vi": "Cô ấy bị lo âu."},
        {"en": "cognitive", "vi": "nhận thức", "pos": "Adj", "pron": "/ˈkɒɡnɪtɪv/", "ex_en": "Cognitive skills develop with age.", "ex_vi": "Kỹ năng nhận thức phát triển theo tuổi."},
        {"en": "motivation", "vi": "động lực", "pos": "N", "pron": "/ˌməʊtɪˈveɪʃn/", "ex_en": "Motivation is key to success.", "ex_vi": "Động lực là chìa khóa của thành công."},
        {"en": "perception", "vi": "nhận thức, tri giác", "pos": "N", "pron": "/pəˈsepʃn/", "ex_en": "Perception affects behavior.", "ex_vi": "Nhận thức ảnh hưởng đến hành vi."},
        {"en": "resilience", "vi": "sự kiên cường", "pos": "N", "pron": "/rɪˈzɪliəns/", "ex_en": "Resilience helps overcome challenges.", "ex_vi": "Sự kiên cường giúp vượt qua thử thách."},
    ],
    "Architecture": [
        {"en": "blueprint", "vi": "bản thiết kế", "pos": "N", "pron": "/ˈbluːprɪnt/", "ex_en": "The architect reviewed the blueprint.", "ex_vi": "Kiến trúc sư đã xem xét bản thiết kế."},
        {"en": "foundation", "vi": "nền móng", "pos": "N", "pron": "/faʊnˈdeɪʃn/", "ex_en": "The foundation is solid.", "ex_vi": "Nền móng rất chắc chắn."},
        {"en": "facade", "vi": "mặt tiền", "pos": "N", "pron": "/fəˈsɑːd/", "ex_en": "The facade was beautifully designed.", "ex_vi": "Mặt tiền được thiết kế đẹp."},
        {"en": "skyscraper", "vi": "nhà chọc trời", "pos": "N", "pron": "/ˈskaɪskreɪpər/", "ex_en": "The skyscraper has 50 floors.", "ex_vi": "Nhà chọc trời có 50 tầng."},
        {"en": "renovation", "vi": "cải tạo", "pos": "N", "pron": "/ˌrenəˈveɪʃn/", "ex_en": "The renovation preserved historical features.", "ex_vi": "Việc cải tạo bảo tồn các đặc trưng lịch sử."},
    ],
}

topic_names = list(vocab_database.keys())

# ============================================================
# PHẦN 4: HÀM SINH DỮ LIỆU
# ============================================================

def make_grammar_wrong(item):
    prompt = f'''Nhiệm vụ của bạn là kiểm tra ngữ pháp và độ tự nhiên của câu tiếng Anh sau đây:
"{item['wrong']}"

Hãy trả về kết quả định dạng JSON với cấu trúc chính xác như sau (KHÔNG dùng markdown code block, KHÔNG có text thừa):
{{
    "is_correct": true/false,
    "error_found": "Mô tả lỗi sai ngữ pháp hoặc chính tả bằng tiếng Việt (nếu is_correct=false, nếu đúng thì để trống)",
    "suggestion": "Câu tiếng Anh đã được sửa đổi cho đúng và tự nhiên nhất",
    "explanation": "Giải thích ngắn gọn quy tắc ngữ pháp tại sao lại sửa như vậy bằng tiếng Việt"
}}'''
    reply = json.dumps({"is_correct": False, "error_found": item['error'], "suggestion": item['correct'], "explanation": item['explain']}, ensure_ascii=False)
    return {"messages": [{"role": "system", "content": "Bạn là một chuyên gia ngôn ngữ học tiếng Anh (English Linguist)."}, {"role": "user", "content": prompt}, {"role": "assistant", "content": reply}]}

def make_grammar_correct(item):
    prompt = f'''Nhiệm vụ của bạn là kiểm tra ngữ pháp và độ tự nhiên của câu tiếng Anh sau đây:
"{item['text']}"

Hãy trả về kết quả định dạng JSON với cấu trúc chính xác như sau (KHÔNG dùng markdown code block, KHÔNG có text thừa):
{{
    "is_correct": true/false,
    "error_found": "Mô tả lỗi sai ngữ pháp hoặc chính tả bằng tiếng Việt (nếu is_correct=false, nếu đúng thì để trống)",
    "suggestion": "Câu tiếng Anh đã được sửa đổi cho đúng và tự nhiên nhất",
    "explanation": "Giải thích ngắn gọn quy tắc ngữ pháp tại sao lại sửa như vậy bằng tiếng Việt"
}}'''
    reply = json.dumps({"is_correct": True, "error_found": "", "suggestion": item['text'], "explanation": item['explain']}, ensure_ascii=False)
    return {"messages": [{"role": "system", "content": "Bạn là một chuyên gia ngôn ngữ học tiếng Anh (English Linguist)."}, {"role": "user", "content": prompt}, {"role": "assistant", "content": reply}]}

def make_vocab(topic_key, count):
    vocabs = vocab_database[topic_key]
    picked = [vocabs[i % len(vocabs)] for i in random.sample(range(100), min(count, len(vocabs)))]
    prompt = f'''Yêu cầu người dùng: "Tạo {count} từ vựng TOEIC chủ đề {topic_key}"
Mỗi từ bắt buộc phải có đầy đủ phiên âm IPA, loại từ, nghĩa tiếng Việt, một câu ví dụ tiếng Anh thực tế, nghĩa tiếng Việt của câu ví dụ và tên chủ đề tương ứng.
BẮT BUỘC chỉ tạo đúng số lượng {count} từ được yêu cầu, KHÔNG ĐƯỢC tạo thừa hoặc thiếu dù chỉ 1 từ.
Trả về dữ liệu dưới dạng JSON là một mảng các object. KHÔNG dùng markdown block.
Cấu trúc mỗi object:
{{
    "english": "từ tiếng Anh",
    "vietnamese": "nghĩa tiếng Việt",
    "pos": "loại từ (N, V, ADJ, ADV, PREP, CONJ)",
    "pronunciation": "phiên âm",
    "example_en": "câu ví dụ tiếng Anh",
    "example_vi": "nghĩa câu ví dụ",
    "topic": "tên chủ đề"
}}'''
    arr = [{"english": v["en"], "vietnamese": v["vi"], "pos": v["pos"], "pronunciation": v["pron"], "example_en": v["ex_en"], "example_vi": v["ex_vi"], "topic": topic_key} for v in picked]
    return {"messages": [{"role": "system", "content": "Bạn là một chuyên gia giáo dục ngôn ngữ. Hãy tạo danh sách từ vựng tiếng Anh chính xác dựa trên yêu cầu của người dùng."}, {"role": "user", "content": prompt}, {"role": "assistant", "content": json.dumps(arr, ensure_ascii=False)}]}

# ============================================================
# PHẦN 5: SINH HƠN 10000 MẪU
# ============================================================
# 80 errors x 80 = 6400
# 40 corrects x 50 = 2000
# 25 topics x 8 counts x 10 = 2000
# Total = 10400 -> trim to 10000

dataset = []

for _ in range(80):
    for item in grammar_errors:
        dataset.append(make_grammar_wrong(item))

for _ in range(50):
    for item in grammar_corrects:
        dataset.append(make_grammar_correct(item))

counts_list = [3, 4, 5, 6, 7, 8, 10, 15]
for _ in range(10):
    for topic_key in topic_names:
        for count in counts_list:
            dataset.append(make_vocab(topic_key, count))

dataset = dataset[:10000]
random.shuffle(dataset)

with open(r'd:\WEB_LEARNENGLISH_PROJECT\ai_training\vocab_dataset.jsonl', 'w', encoding='utf-8') as f:
    for data in dataset:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')

print(f"Done! Total samples: {len(dataset)}")

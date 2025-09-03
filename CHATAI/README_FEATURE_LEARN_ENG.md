## FEATURE 2: điều chỉnh giao diện cho mobile web
- đọc phần feature 2 của trang @README_FEATURE_LEARN_ENG.md và thêm code trong vocabulary trong thư mục learn_eng, không cần thêm nút, mà khi đọc từ vựng xong, thì dịch và đọc phần dịch sang tiếng việt của từ đó. (status:DONE)
- sửa lại 1 chút, từ vựng "word" là có rồi, nó cũng có đọc , level cũng có, file âm thanh Uk, US không cần, example cũng có rồi, meaning cũng có, vì vậy, còn lại các thông tin khác thì thêm vào. Không, ý tôi là có các thông tin này rồi:
"
word, meaning, definition, example, vi_du, spelling, example_vi, vi_du_vi, level, audio_uk, audio_us.
"
vì vậy chỉ cần thêm các field còn thiếu và thể hiện. 
Và font chữ cần phải đều, cân đối.

- Trang vào @entry_screen có vẻ chưa chuyên nghiệp và sinh động, hãy làm nó sinh động hơn đi, giống như dashboard là tôi thấy hay đó. Nhưng mỗi trang cần có thiết kế khác biệt nhưng nhất quán với nhau. Status: DONE.

nút âm thanh trong @vocabulary_practice_screen.dart cần thể hiện đang play hoặc đang dừng để người dùng dễ nhận biết. Status: DONE.

hiện tại tôi thấy process trong practice có process là 58/1076 nhưng lession process lại ghi 52/1076. Cần kiểm tra lại. Tôi nghĩ là lấy số từ page process (52/1076) là trang @vocabulary_progress_controller.dart làm chuẩn. Sau đó, khi vào page practice thì lấy thông tin của process cho đồng bộ. 
@vocabulary_practice_screen.dart @vocabulary_practice_controller.dart @vocabulary_progress_controller.dart @vocabulary_lesson_list_screen.dart.
Status: DONE.

- Nhưng sau khi đọc qua từ mới, thì tôi quay lại trang process thì không thấy cập nhật lại vậy.


 // if (state == null || state?.currentIndex == null) return;

        // final currentIndex = state.currentIndex!;

        // // Handle first word case
        // // va luu lai
        // if (currentIndex == 0 && currentWordIndex.value == 0) {
        //   markCurrentWordAsHeard();
        //   showMeaning.value = true;
        //   speakingText.value = null;
        //   saveProgress(currentWordIndex.value);
        //   return;
        // }

        // if (currentIndex > 0 && currentWordIndex.value == 0) {
        //   // Handle subsequent words
        //   if ((currentIndex - 3) % (1) == 0) {
        //     print('currentIndex-C1---${currentIndex}');
        //     _updateWordProgress();
        //   }
        //   return;
        // }

        // if (currentIndex >= words.length ||
        //     currentIndex < currentWordIndex.value) {
        //   return;
        // }

        // // Handle subsequent words
        // if ((currentIndex - 3) % (currentWordIndex.value) == 0) {
        //   print('currentIndex--${currentIndex}');
        //   _updateWordProgress();
        // }
---
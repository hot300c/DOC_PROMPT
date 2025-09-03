## FEATURE 2: điều chỉnh giao diện cho mobile web
- nếu vào menu chat thì hiển thị 2 icon trên app bar home, và đổi title là Chat Advance. (Status: DONE)
- tôi muốn sửa lại trang @chat_box_input_widget.dart  giống như hình nhé. Không cần các button bên dưới. Có bo viền, và thiết kế thiệt chuyên nghiệp nhé.
- Danh sách chat trong trang @chat

vẫn còn bị, sau khi tôi bấm vào ô nhập liệu thì ô nó dâng lên để hiện bàn phím ảo rồi đột ngột nó kéo xuống đáy dưới màn hình mà không để tôi bấm bàn phím ảo được
---

TROUBLESHOOT:

BI CHỖ NÀY BỊ BÀN PHÍM ẢO:
phải comment lại thì hết bị:

  // final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final TaskListController tlController = Get.find<TaskListController>();

  ChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // final size = MediaQuery.of(context).size;
    // final isSmallScreen = size.width < 600;
    // final chatController = Get.find<ChatProvider>();


    return Scaffold(
      // key: _scaffoldKey,
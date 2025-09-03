Đây là chức năng RAG.
Path: lib/features/rag

Lưu ý: Status: DONE. nghĩa là đã hoàn tất

## FEATURE 1:
- kiểm tra lại toàn bộ các trang trong thư mục rag, đảm bảo tuân thủ đúng kiến trúc, rõ ràng, và validation đầy đủ
- khi thu nhỏ responsive mobile web, thì menu cấp 2 sẽ là dạng droplist, để khi người dùng chọn doanh nghiệp khác thì droplist refesh để mở lại trang. Dưới droplist là màn hình tương ứng.
- [ ] Đảm bảo mọi màn hình đều dùng controller/provider, không viết logic trong UI
- [ ] Tất cả form đều có validator, error message rõ ràng
- [ ] Menu cấp 2 responsive: droplist trên mobile web, sidebar trên desktop
- [ ] Khi chọn doanh nghiệp, droplist refresh và load lại màn hình dưới
- Chuyển menu cấp 2 sang droplist responsive mobile web
- Cần xoá lỗi mouse_tracker. Sau đó, chỉnh menu rag left side bar thành menu droplist nằm ngang cho giao diện mobile web.

---

## FEATURE 2: phần này điều chỉnh cho mobile web
- menu rag left side bar nằm ngang, dạng sổ xuống để chọn.
Status: DONE
- tôi chưa thấy @RagLeftSidebarWidget hiển thị trên giao diện, hãy kiểm tra.
Status: DONE
- kiểm tra và điều chỉnh trang @rag_apikey_screen.dart  hỗ trợ responsive cho web mobile nhé.
Status: DONE
- nó chỉ bị khi tôi vào các trang @rag_screen.dart @rag_apikey_screen.dart @rag_left_sidebar_widget.dart. Status: DONE
- Giao diện API Key mobile web cần điều chỉnh lại cho cân đối. Status: DONE
- Tiếp tục giao diện oganization, log, playground mobile web cần điều chỉnh lại cho cân đối như page API Key. Status: DONE
- trong trang @rag_botagent_screen.dart , phần mục add agent nên chuyển thành drawer để show ở phía phải, và có icon phía phải để người dùng bấm thì show ra. Status: DONE
- giờ phần @rag_right_side_one.dart sẽ ẩn khi ở chế độ mobile web trong trang @rag_botagent_screen.dart. Status: DONE
- chỉnh trang @rag_enterprise_editting cho cân đối.
- trang @rag_botagent_screen.dart nên kiểm tra lại, chỉnh cân đối và font chữ đều, đẹp, dễ nhìn.
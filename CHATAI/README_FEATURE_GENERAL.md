## FEATURE 1: đổi version cache

Giải pháp tốt nhất: Cache Busting (xoá cache khi có phiên bản mới)
1. Thay đổi tên file build (hash)
Flutter web mặc định đã sinh ra file main.dart.js với hash, nhưng một số file (manifest, favicon, v.v.) vẫn có thể bị cache.
Nếu bạn dùng hosting tĩnh (Firebase, Vercel, Netlify, v.v.), hãy đảm bảo không cache lâu các file HTML, manifest, service worker.
2. Thêm version/hash vào index.html
Thêm query string version vào file JS/CSS trong web/index.html:
 Status: DONE

Hướng dẫn cập nhật version tự động trong GitHub Actions
1. Ý tưởng
Sử dụng một bước trong workflow để thay thế giá trị của meta tag app-version trong web/index.html bằng giá trị mới (ví dụ: ngày giờ build, commit hash, hoặc số build). Status: DONE
---

## FEATURE 2: điều chỉnh giao diện cho mobile web
2.1 - Menu side bar ở mobile web là thành biểu tượng Hambuger. Khi click vào thì hiển thị menu dọc như hiện tại.  Status: DONE
2.2 - Trong page Chat, Nút "Create new chat " ở mobile web nên đặt trên cùng bên phải ngang với nút Menu Hambuger. Status: DONE
2.3 - "Danh sách Chat"  ở mobile web nên là nút đặt kế bên bên trái nút thêm, để khi người dùng bấm nút thì nó hiển thị như page Setting. Status: DONE
2.4 - Khi bấm vào menu Hambuger, mà đã thực hiện xong ở 2.2, thì hiển thị tên page theo menu đã bấm. Và có icon menu rag như đã thiết kế. Status: DONE
- "Mobile Web AppBar & Drawer Navigation". Status: DONE
- "Responsive Drawer & RAG Menu for Mobile Web". Status: DONE
- "Unified Mobile Navigation: Hamburger & RAG Drawer". Status: DONE
- icon menu rag chỉ hiển thị khi người dùng bấm click vào rag trong danh sách menu ở hamburger. Status: DONE
- Chuyển các title trong các trang Rag để thay thế title Home, sau đó bỏ các appbar trong các trang rag.  Status: DONE
- điều chỉnh trong vùng drawer khi bấm menu rag nhìn cho đẹp, chuyên nghiệp và có icon nổi bật theo theme dark và light nhé.  Status: DONE

- tại trang home, khi  chọn item apikey thì hiện title thay cho chữ default là home
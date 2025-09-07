#!/usr/bin/env python3
import re

# Read the markdown file
with open('HOP_DONG_OUTSOURCE_RUTGON_PDF.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Create professional HTML structure
html_template = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HỢP ĐỒNG GIA CÔNG PHẦN MỀM - LMA</title>
    <link rel="stylesheet" href="professional-contract.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <header id="title-block-header">
        <h1 class="title">HỢP ĐỒNG GIA CÔNG PHẦN MỀM</h1>
        <p class="subtitle">LOAN MANAGEMENT APP (LMA)</p>
        <p class="author">Công ty TNHH PT&N Solution</p>
        <p class="date">2024</p>
    </header>

    <div class="contract-info">
        <p><strong>Số hợp đồng:</strong> PTN-LMA-2024-001</p>
        <p><strong>Ngày ký:</strong> [Ngày] tháng [Tháng] năm [Năm]</p>
        <p><strong>Địa điểm ký:</strong> [Địa điểm]</p>
    </div>

    <div class="party-section">
        <h2>BÊN A (BÊN THUÊ GIA CÔNG): [TÊN CÔNG TY ĐỐI TÁC]</h2>
        <table>
            <tr><td><strong>Tên công ty</strong></td><td>[Tên công ty đối tác]</td></tr>
            <tr><td><strong>Địa chỉ</strong></td><td>[Địa chỉ đầy đủ]</td></tr>
            <tr><td><strong>Mã số thuế</strong></td><td>[MST]</td></tr>
            <tr><td><strong>Đại diện</strong></td><td>[Tên đại diện]</td></tr>
            <tr><td><strong>Chức vụ</strong></td><td>[Chức vụ]</td></tr>
            <tr><td><strong>Điện thoại</strong></td><td>[SĐT]</td></tr>
            <tr><td><strong>Email</strong></td><td>[Email]</td></tr>
            <tr><td><strong>Tài khoản ngân hàng</strong></td><td>[Số tài khoản]</td></tr>
        </table>
    </div>

    <div class="party-section">
        <h2>BÊN B (BÊN GIA CÔNG): CÔNG TY TNHH PT&N SOLUTION</h2>
        <table>
            <tr><td><strong>Tên công ty</strong></td><td>Công ty TNHH PT&N Solution</td></tr>
            <tr><td><strong>Địa chỉ</strong></td><td>[Địa chỉ công ty PT&N Solution]</td></tr>
            <tr><td><strong>Mã số thuế</strong></td><td>[MST]</td></tr>
            <tr><td><strong>Đại diện</strong></td><td>[Tên đại diện]</td></tr>
            <tr><td><strong>Chức vụ</strong></td><td>[Chức vụ]</td></tr>
            <tr><td><strong>Điện thoại</strong></td><td>[SĐT]</td></tr>
            <tr><td><strong>Email</strong></td><td>[Email]</td></tr>
            <tr><td><strong>Tài khoản ngân hàng</strong></td><td>[Số tài khoản]</td></tr>
        </table>
    </div>

    <h2>ĐIỀU 1: ĐỊNH NGHĨA VÀ GIẢI THÍCH</h2>
    <h3>1.1 Định nghĩa</h3>
    <ul>
        <li><strong>"Dự án"</strong> có nghĩa là Ứng dụng Quản lý Khoản vay (Loan Management App - LMA) được mô tả trong tài liệu kỹ thuật đính kèm.</li>
        <li><strong>"Giai đoạn 1"</strong> có nghĩa là giai đoạn phát triển các tính năng cơ bản của ứng dụng LMA theo phạm vi công việc đã thỏa thuận.</li>
        <li><strong>"Yêu cầu phát sinh"</strong> có nghĩa là bất kỳ yêu cầu bổ sung, thay đổi hoặc mở rộng nào ngoài phạm vi công việc ban đầu đã được thỏa thuận.</li>
        <li><strong>"Deliverables"</strong> có nghĩa là tất cả các sản phẩm, tài liệu và dịch vụ mà Bên B phải cung cấp theo hợp đồng này.</li>
        <li><strong>"Source Code"</strong> có nghĩa là mã nguồn của phần mềm, bao gồm tất cả các file code, database schema, configuration files và documentation.</li>
    </ul>

    <h3>1.2 Tài liệu tham chiếu</h3>
    <ul>
        <li>Tất cả các yêu cầu kỹ thuật, chi phí và timeline được mô tả trong tài liệu đính kèm sẽ được áp dụng cho hợp đồng này.</li>
    </ul>

    <h2>ĐIỀU 2: PHẠM VI CÔNG VIỆC</h2>
    <h3>2.1 Giai đoạn 1 - Phát triển cơ bản</h3>
    <p>Bên B sẽ phát triển ứng dụng LMA với các tính năng sau:</p>

    <div class="core-features">
        <h4>2.1.1 Ứng dụng di động đa nền tảng</h4>
        <ul>
            <li><strong>Flutter Framework</strong> cho cross-platform development</li>
            <li><strong>iOS:</strong> Hỗ trợ iOS 13.0+ (iPhone, iPad)</li>
            <li><strong>Android:</strong> Hỗ trợ Android 8.0+ (API level 26)</li>
            <li><strong>Web:</strong> Progressive Web App (PWA) support</li>
        </ul>

        <h4>2.1.3 Core Features</h4>
        <div class="feature-grid">
            <div class="feature-item">
                <h5>User Account Management</h5>
                <p>Registration, Login/Logout, Password Reset, Profile Edit - Secure access với dashboard entry point</p>
            </div>
            <div class="feature-item">
                <h5>Dashboard (Home)</h5>
                <p>Loan summary cards, Total balance, Active loans count - Quick action buttons - Central hub showing high-level loan status & actions</p>
            </div>
            <div class="feature-item">
                <h5>Loan Application & Approval</h5>
                <p>Application form, Status tracking, Document upload (optional) - Approval updates - Submission + feedback loop; UI flow matches Credora style</p>
            </div>
            <div class="feature-item">
                <h5>Repayment Schedule</h5>
                <p>Repayment calendar, Upcoming installments, Total due - Visual calendar or list user-friendly view, mirror Credora styling</p>
            </div>
            <div class="feature-item">
                <h5>Repayment Reminder</h5>
                <p>Email/SMS reminders, Alert banners in dashboard for due dates - Keep users on track with due repayment alerts</p>
            </div>
            <div class="feature-item">
                <h5>Push Notifications</h5>
                <p>Loan approval updates, Repayment due reminders, General alerts - Enhances UX, instant feedback to user</p>
            </div>
            <div class="feature-item">
                <h5>Admin Panel</h5>
                <p>User/loan management, View status, Reports, CSV export - Dashboard-like view; clear tables/cards for managing backend</p>
            </div>
            <div class="feature-item">
                <h5>Wallet / Balance View</h5>
                <p>Wallet balance, Fund disbursal tracking, Transaction history - Balance card & transactions (similar to Credora's wallet card)</p>
            </div>
        </div>
    </div>

    <h2>ĐIỀU 3: TIMELINE VÀ MILESTONE</h2>
    <h3>3.1 Tổng thời gian dự án: <strong>2,5 tháng</strong></h3>

    <div class="timeline-section">
        <h3>3.2 Các giai đoạn chính:</h3>
        
        <div class="phase-section">
            <h4>Phase 1: Project Setup & Core Infrastructure (3 tuần)</h4>
            <p><strong>Công việc:</strong></p>
            <ul>
                <li>Thiết lập project structure</li>
                <li>Cài đặt development environment</li>
                <li>Database design và migration</li>
                <li>Basic authentication system</li>
                <li>User Account Management (Registration, Login/Logout, Password Reset)</li>
            </ul>
            <div class="deliverables">
                <p><strong>Deliverables:</strong></p>
                <ul>
                    <li>Project structure hoàn chỉnh</li>
                    <li>Development environment setup</li>
                    <li>Basic authentication system</li>
                    <li>Database schema</li>
                    <li>User Account Management features</li>
                </ul>
            </div>
        </div>

        <div class="phase-section">
            <h4>Phase 2: Core Features & Loan Management (4 tuần)</h4>
            <p><strong>Công việc:</strong></p>
            <ul>
                <li>Profile Edit và dashboard entry point</li>
                <li>Dashboard (Home) với loan summary cards, total balance, active loans count</li>
                <li>Quick action buttons</li>
                <li>Loan Application & Approval workflow</li>
                <li>Document upload system</li>
                <li>Status tracking</li>
                <li>Approval updates</li>
                <li>Repayment Schedule với calendar view</li>
                <li>Upcoming installments display</li>
                <li>Total due calculation</li>
            </ul>
            <div class="deliverables">
                <p><strong>Deliverables:</strong></p>
                <ul>
                    <li>Complete dashboard system</li>
                    <li>Loan application & approval system</li>
                    <li>Repayment schedule functionality</li>
                    <li>Document management</li>
                    <li>50% progress completion</li>
                </ul>
            </div>
        </div>

        <div class="phase-section">
            <h4>Phase 3: Advanced Features & Finalization (3 tuần)</h4>
            <p><strong>Công việc:</strong></p>
            <ul>
                <li>Repayment Reminder system (Email/SMS)</li>
                <li>Alert banners in dashboard</li>
                <li>Push Notifications (Firebase FCM)</li>
                <li>Admin Panel với user/loan management</li>
                <li>Reports và CSV export</li>
                <li>Wallet / Balance View</li>
                <li>Fund disbursal tracking</li>
                <li>Transaction history</li>
                <li>Mobile app development</li>
                <li>Responsive web interface</li>
                <li>UI/UX implementation (Credora style)</li>
                <li>Cross-platform testing</li>
                <li>Performance optimization</li>
                <li>Comprehensive testing</li>
                <li>Security testing</li>
                <li>Production deployment</li>
                <li>Documentation</li>
            </ul>
            <div class="deliverables">
                <p><strong>Deliverables:</strong></p>
                <ul>
                    <li>Complete notification & reminder system</li>
                    <li>Admin panel functionality</li>
                    <li>Wallet & balance features</li>
                    <li>Complete mobile applications</li>
                    <li>Web application</li>
                    <li>Fully tested application</li>
                    <li>Production deployment</li>
                    <li>Complete documentation</li>
                    <li>80% progress completion</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="milestone-table">
        <h3>3.3 Milestone Payments</h3>
        <table>
            <thead>
                <tr>
                    <th>Phase</th>
                    <th>Payment %</th>
                    <th>Amount (AUD)</th>
                    <th>Condition / Deliverable</th>
                    <th>Notes</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Phase 1</td>
                    <td>60%</td>
                    <td>1,800 AUD</td>
                    <td>Agreement on scope & requirements; project kick-off</td>
                    <td>Initial development begins</td>
                </tr>
                <tr>
                    <td>Phase 2</td>
                    <td>20%</td>
                    <td>600 AUD</td>
                    <td>50% progress OR completion of User Management & Loan modules</td>
                    <td>Core features in place</td>
                </tr>
                <tr>
                    <td>Phase 3</td>
                    <td>20%</td>
                    <td>600 AUD</td>
                    <td>80% progress and delivery of remaining functionalities</td>
                    <td>Final handover, testing & closure</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="cost-section">
        <h2>ĐIỀU 4: CHI PHÍ VÀ THANH TOÁN</h2>
        <h3>4.1 Tổng giá trị hợp đồng: <strong>3,000 AUD</strong></h3>

        <div class="cost-breakdown">
            <h3>4.2 Chi phí breakdown:</h3>
            <h4>4.2.1 Development Cost: 3,000 AUD</h4>
            <table>
                <thead>
                    <tr>
                        <th>Hạng mục</th>
                        <th>Chi phí (AUD)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Backend development</td>
                        <td>1,500</td>
                    </tr>
                    <tr>
                        <td>Mobile app development</td>
                        <td>1,000</td>
                    </tr>
                    <tr>
                        <td>Web application</td>
                        <td>300</td>
                    </tr>
                    <tr>
                        <td>Integration & testing</td>
                        <td>200</td>
                    </tr>
                    <tr>
                        <td><strong>Tổng cộng</strong></td>
                        <td><strong>3,000</strong></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <h3>4.3 Chi phí server (Bên A tự chịu):</h3>
        <table>
            <thead>
                <tr>
                    <th>STT</th>
                    <th>Danh mục</th>
                    <th>Chi phí</th>
                    <th>Ghi chú</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td><strong>AWS EC2 t3.large (Admin Backend)</strong></td>
                    <td>~$47 USD/tháng</td>
                    <td>2 vCPU, 8 GiB RAM</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td><strong>Apple Developer Program (Organization)</strong></td>
                    <td>~$99 USD/năm</td>
                    <td>Bắt buộc cho iOS</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td><strong>Google Play Developer Account</strong></td>
                    <td>~$25 USD (một lần)</td>
                    <td>Bắt buộc cho Android</td>
                </tr>
                <tr>
                    <td>4</td>
                    <td><strong>Push Notification (Firebase FCM)</strong></td>
                    <td>$0</td>
                    <td>Free tier</td>
                </tr>
            </tbody>
        </table>
        <p><strong>Tổng chi phí server hàng tháng:</strong> ~$47 USD/tháng<br>
        <strong>Tổng chi phí server năm đầu:</strong> ~$564 USD/năm</p>

        <h3>4.4 Chi phí vận hành & hỗ trợ (Bên A tự chịu):</h3>
        <table>
            <thead>
                <tr>
                    <th>STT</th>
                    <th>Danh mục</th>
                    <th>Chi phí</th>
                    <th>Ghi chú</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td><strong>Maintenance & Support</strong></td>
                    <td>300 AUD/tháng</td>
                    <td>Bug fixing, updates, working-hour monitoring. Recommended minimum 12-month contract.</td>
                </tr>
            </tbody>
        </table>
        <p><strong>Tổng chi phí vận hành & hỗ trợ:</strong> 300 AUD/tháng<br>
        <strong>Tổng chi phí vận hành & hỗ trợ năm đầu:</strong> 3,600 AUD/năm</p>
    </div>

    <div class="signature-section">
        <h2>ĐIỀU 14: KÝ KẾT</h2>
        <p>Hợp đồng này có hiệu lực từ ngày ký và được lập thành <strong>02 (hai) bản</strong> có giá trị pháp lý như nhau, mỗi bên giữ <strong>01 (một) bản</strong>.</p>
        
        <div class="signature-blocks">
            <div class="signature-block">
                <h4>BÊN A (BÊN THUÊ GIA CÔNG)</h4>
                <div class="signature-line"></div>
                <p>[Tên đại diện]<br>[Chức vụ]<br>[Ký tên và đóng dấu]</p>
            </div>
            
            <div class="signature-block">
                <h4>BÊN B (BÊN GIA CÔNG)</h4>
                <div class="signature-line"></div>
                <p>[Tên đại diện]<br>[Chức vụ]<br>[Ký tên và đóng dấu]</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p><strong>Ngày:</strong> [Ngày] &nbsp;&nbsp;&nbsp; <strong>Tháng:</strong> [Tháng] &nbsp;&nbsp;&nbsp; <strong>Năm:</strong> [Năm]</p>
        </div>
    </div>

    <div class="contract-footer">
        <p><strong>Lưu ý:</strong> Hợp đồng này được soạn thảo dựa trên tài liệu kỹ thuật và yêu cầu chi tiết của dự án Loan Management App. Tất cả các điều khoản đều có thể được điều chỉnh theo thỏa thuận giữa hai bên.</p>
        <p><strong>Công ty TNHH PT&N Solution cam kết cung cấp dịch vụ gia công phần mềm chất lượng cao với giá cả cạnh tranh và hỗ trợ kỹ thuật tận tình.</strong></p>
    </div>
</body>
</html>'''

# Write the HTML file
with open('HOP_DONG_OUTSOURCE_RUTGON_PROFESSIONAL_FINAL.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ Professional HTML file created successfully!")

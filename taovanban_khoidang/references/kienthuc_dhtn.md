# BỘ KIẾN THỨC HỆ THỐNG ĐIỀU HÀNH TÁC NGHIỆP (DHTN)
# Phiên bản: 1.0 | Cập nhật: 09/07/2026
# Mục đích: Tài liệu tham chiếu chuẩn cho chatbot AI hỗ trợ người dùng hệ thống ĐHTN

---

## MỤC LỤC

1. [Giới thiệu hệ thống](#1-giới-thiệu-hệ-thống)
2. [Đăng nhập và Trang chủ](#2-đăng-nhập-và-trang-chủ)
3. [Vai trò người dùng](#3-vai-trò-người-dùng)
4. [Module Văn bản đến](#4-module-văn-bản-đến)
5. [Module Văn bản đi](#5-module-văn-bản-đi)
6. [Module Phiếu trình](#6-module-phiếu-trình)
7. [Module Quản lý nhiệm vụ](#7-module-quản-lý-nhiệm-vụ)
8. [Module Lịch họp](#8-module-lịch-họp)
9. [Module Quản lý hồ sơ](#9-module-quản-lý-hồ-sơ)
10. [Module Tài liệu cá nhân](#10-module-tài-liệu-cá-nhân)
11. [Module Văn bản công khai](#11-module-văn-bản-công-khai)
12. [Module Theo dõi KPI](#12-module-theo-dõi-kpi)
13. [Module Quản trị hệ thống](#13-module-quản-trị-hệ-thống)
14. [Xử lý sự cố thường gặp](#14-xử-lý-sự-cố-thường-gặp)
15. [Quy tắc an toàn và bảo mật](#15-quy-tắc-an-toàn-và-bảo-mật)
16. [Câu hỏi thường gặp (FAQ)](#16-câu-hỏi-thường-gặp-faq)

---

## 1. GIỚI THIỆU HỆ THỐNG

### 1.1. Hệ thống là gì?
- **Tên đầy đủ:** Hệ thống Điều hành tác nghiệp các cơ quan Đảng
- **Tên viết tắt:** ĐHTN hoặc DHTN
- **Địa chỉ truy cập:** https://dhtn.dcs.vn
- **Mục đích:** Số hóa toàn bộ quy trình xử lý văn bản đến, văn bản đi, phiếu trình, quản lý nhiệm vụ, lịch họp và hồ sơ công việc trong nội bộ các cơ quan Đảng.
- **Đối tượng sử dụng:** Cán bộ, công chức, viên chức làm việc tại các cơ quan Đảng các cấp.

### 1.2. Công nghệ và nền tảng
- **Nền tảng phát triển:** ZK Framework (sử dụng file định dạng `.zul`)
- **Giao diện:** Bộ giao diện mẫu Admin-Ex — tối giản, trực quan
- **Trình duyệt tương thích:** Google Chrome hoặc Microsoft Edge phiên bản mới nhất (khuyến nghị). Các trình duyệt khác có thể gây lỗi hiển thị bảng biểu ZK.

### 1.3. Cấu trúc giao diện chính
Giao diện hệ thống được chia thành 3 vùng chính:

| Vùng | Vị trí | Mô tả |
|------|--------|-------|
| **Thanh công cụ trên cùng (Top Nav)** | Trên cùng, nền đỏ | Hiển thị tên đơn vị, nút tìm kiếm 🔍, thông báo 🔔, làm mới 🔄. Bấm vào tên người dùng ở góc phải để đổi mật khẩu hoặc đăng xuất. |
| **Menu bên trái (Sidebar)** | Bên trái | Cấu trúc cây thư mục phân cấp, chứa tất cả các chức năng chính mà người dùng được phân quyền. Bấm vào tên chức năng để mở. |
| **Khu vực làm việc trung tâm** | Giữa | Hiển thị dưới dạng các tab đa nhiệm — cho phép mở nhiều chức năng cùng lúc và chuyển đổi nhanh. Bấm X trên tab để đóng. |

---

## 2. ĐĂNG NHẬP VÀ TRANG CHỦ

### 2.1. Cách đăng nhập vào hệ thống
**Điều kiện tiên quyết:** Có tài khoản (tên đăng nhập + mật khẩu) do quản trị viên cấp.
* **Mật khẩu mặc định:** Đối với tài khoản mới khởi tạo, mật khẩu mặc định là **`222222aA+`** (gồm 6 số 2, ký tự `a` thường, `A` hoa và dấu `+`).
* **Lưu ý đăng nhập lần đầu:** Người dùng nhập mã OTP được gửi về số điện thoại đăng ký, sau đó hệ thống sẽ yêu cầu thay đổi mật khẩu mặc định sang mật khẩu cá nhân mới.
* **Thời gian lưu phiên đăng nhập:** Phiên đăng nhập qua OTP sẽ được trình duyệt ghi nhớ trong vòng **30 ngày** (nếu đổi trình duyệt hoặc xóa cookie/cache sẽ cần xác thực lại).

**Các bước thực hiện:**
1. Mở trình duyệt **Google Chrome** hoặc **Microsoft Edge** trên máy tính.
2. Gõ vào thanh địa chỉ: `https://dhtn.dcs.vn` rồi nhấn **Enter**.
3. Tại ô **"Tên tài khoản"** — nhập số điện thoại hoặc tên đăng nhập đã được cấp.
4. Tại ô **"Mật khẩu"** — nhập mật khẩu. Bấm biểu tượng 👁 bên phải để kiểm tra mật khẩu đã đúng chưa.
5. Bấm nút **"Đăng nhập"** màu đỏ.

**Đăng nhập bằng VNeID:** Ngoài tài khoản thông thường, người dùng có thể đăng nhập bằng **VNeID** (nút phía dưới). Liên hệ bộ phận IT để được hướng dẫn kích hoạt VNeID.

**Khi quên mật khẩu:**
- Bấm vào chữ **"Quên mật khẩu"** trên màn hình đăng nhập.
- Hoặc liên hệ trực tiếp quản trị viên hệ thống để được reset mật khẩu.
- **KHÔNG** chia sẻ mật khẩu cho bất kỳ ai.

### 2.2. Trang chủ (Dashboard)
Sau khi đăng nhập thành công, màn hình Trang chủ hiển thị các thông tin tổng quan:

| Vùng trên Trang chủ | Mô tả chi tiết |
|---------------------|----------------|
| **Menu bên trái** | Danh sách tất cả chức năng: Văn bản đến, Văn bản đi, Phiếu trình, Lịch họp, Nhiệm vụ... Bấm vào tên chức năng để mở. |
| **Thanh trên cùng (đỏ)** | Hiển thị tên đơn vị, nút tìm kiếm 🔍, thông báo 🔔, làm mới 🔄. Bấm vào tên bạn ở góc phải để đổi mật khẩu hoặc đăng xuất. |
| **Các ô thống kê** | Số lượng văn bản đến/đi/phiếu trình theo trạng thái. **Bấm trực tiếp vào con số** để mở danh sách tương ứng — rất nhanh! |
| **Nhiệm vụ nhận được** | Biểu đồ tiến độ nhiệm vụ cá nhân — giúp nắm nhanh tổng quan công việc được giao. |
| **Lịch họp sắp tới** | Hiển thị các cuộc họp trong tuần cần tham dự. |
| **Các tab phía trên** | Mỗi chức năng mở ra sẽ là một tab riêng. Có thể chuyển qua lại hoặc bấm X để đóng tab. |

### 2.3. Đăng xuất
1. Bấm vào **tên của bạn** ở góc trên bên phải.
2. Chọn **"Đăng xuất"** từ menu xổ xuống.

> **QUAN TRỌNG:** Luôn đăng xuất khi rời khỏi máy tính, đặc biệt trên máy dùng chung, để bảo vệ tài khoản.

---

## 3. VAI TRÒ NGƯỜI DÙNG

Hệ thống phân chia quyền hạn chặt chẽ dựa trên 3 vai trò chính ở cấp phòng ban/đơn vị cơ sở:

### 3.1. Văn thư (Clerk)
- **Nhiệm vụ chính:** Tiếp nhận văn bản đến từ các cơ quan bên ngoài, vào sổ văn bản, trình Lãnh đạo phân phối; thực hiện cấp số, đóng dấu số (chữ ký số) và ban hành văn bản đi chính thức.
- **Các module thường dùng:** Sổ văn bản đến, Cấp số văn bản đi, Phát hành văn bản, Quản lý sổ văn bản.
- **Đặc thù:** Là đầu mối tiếp nhận và ban hành văn bản, thực hiện đóng dấu chữ ký số trên văn bản đi.

### 3.2. Lãnh đạo (Leader)
- **Nhiệm vụ chính:** Xem xét, phê duyệt phiếu trình; chỉ đạo, phân phối văn bản đến cho các phòng ban/chuyên viên; ký duyệt dự thảo văn bản đi; giao nhiệm vụ và giám sát tiến độ công việc.
- **Các module thường dùng:** Duyệt phiếu trình, Bút phê văn bản đến, Ký duyệt văn bản đi, Giao nhiệm vụ.
- **Đặc thù:** Có quyền phân phối, ký duyệt và giao nhiệm vụ; có thể xem báo cáo tiến độ của cấp dưới.

### 3.3. Chuyên viên (Specialist)
- **Nhiệm vụ chính:** Tiếp nhận và xử lý trực tiếp văn bản đến theo chỉ đạo; soạn thảo dự thảo văn bản đi trình ký; tạo phiếu trình đề xuất công việc; báo cáo tiến độ thực hiện nhiệm vụ được giao.
- **Các module thường dùng:** Văn bản đến tôi, Dự thảo của tôi, Phiếu trình của tôi, Danh sách nhiệm vụ, Tài liệu cá nhân.
- **Đặc thù:** Thực hiện xử lý trực tiếp các công việc chuyên môn; không có quyền phát hành hoặc cấp số văn bản.

---

## 4. MODULE VĂN BẢN ĐẾN

### 4.1. Tổng quan
Module Văn bản đến quản lý toàn bộ vòng đời của văn bản gửi đến cơ quan, từ lúc tiếp nhận đến khi hoàn thành.

**Luồng xử lý chuẩn:**
`Văn thư tiếp nhận → Vào sổ văn bản → Trình Lãnh đạo → Lãnh đạo bút phê phân phối → Chuyên viên xử lý → Hoàn thành/Lưu hồ sơ`

**Các chức năng con trong menu:**

| Chức năng con | Ý nghĩa | Đường dẫn menu |
|--------------|---------|---------------|
| Văn bản chờ xử lý | Danh sách văn bản mới chuyển đến bạn, **chưa xử lý xong** | VĂN BẢN ĐẾN → Văn bản chờ xử lý |
| Văn bản đã xử lý | Văn bản bạn **đã chuyển tiếp** hoặc **đã hoàn thành** | VĂN BẢN ĐẾN → Văn bản đã xử lý |
| Văn bản bị trả lại | Văn bản bạn chuyển nhưng người nhận **trả lại** | VĂN BẢN ĐẾN → Văn bản đề nghị trả lại |
| Văn bản nhận để biết | Văn bản gửi cho bạn **chỉ để nắm thông tin** (không cần xử lý) | VĂN BẢN ĐẾN → Nhận để biết |
| Tra cứu VB đến tôi | Tìm kiếm nâng cao trong **toàn bộ** VB đến | VĂN BẢN ĐẾN → Tra cứu VB đến tôi |

### 4.2. Các trạng thái văn bản đến
- **Chờ xử lý:** Văn bản được chuyển đến tài khoản của bạn và chưa được xác nhận hoàn thành.
- **Đã xử lý:** Văn bản đã được chuyển tiếp cho người khác hoặc đã bấm xác nhận hoàn thành.
- **Đề nghị trả lại:** Văn bản bị người nhận từ chối/trả lại do không đúng thẩm quyền xử lý.

### 4.3. Cách tìm kiếm văn bản đến

**Tìm kiếm nhanh (lọc trực tiếp trên bảng):**
1. Nhìn lên phía trên bảng danh sách, thấy các ô trống nhỏ nằm dưới tiêu đề của mỗi cột (Số ký hiệu, Trích yếu...).
2. Gõ trực tiếp từ khóa vào ô tương ứng (ví dụ: gõ `12-HD/TW` vào cột "Số, ký hiệu" hoặc gõ `Đại hội` vào cột "Trích yếu nội dung").
3. Danh sách tự động lọc kết quả ngay lập tức khi gõ.

**Tìm kiếm nâng cao:**
1. Bấm vào nút **"Tìm kiếm nâng cao"** (biểu tượng kính lúp đỏ ở góc trên bên phải của bảng).
2. Hộp thông tin hiện ra, điền khoảng thời gian, cơ quan ban hành, độ khẩn/mật...
3. Bấm nút **"Tìm kiếm"**.

**Làm mới danh sách:**
- Xóa chữ đã gõ trong các ô lọc.
- Hoặc bấm nút **"Làm mới"** (biểu tượng 2 mũi tên xoay tròn) trên thanh công cụ.

**Tra cứu toàn bộ:**
- Sử dụng chức năng **"Tra cứu VB đến tôi"** (VĂN BẢN ĐẾN → Tra cứu VB đến tôi) để tìm theo nhiều tiêu chí:
  - Số đến, Số ký hiệu, Ngày văn bản
  - Cơ quan ban hành, Loại văn bản
  - Trích yếu nội dung, Độ khẩn, Độ mật
  - Trạng thái xử lý (Đã đọc/Chưa đọc, Đã hoàn thành/Chưa hoàn thành)
- Đây là công cụ tìm kiếm **mạnh nhất** trong module Văn bản đến — dùng khi cần tìm lại văn bản cũ từ nhiều tháng trước.

### 4.4. Cách đọc và tải file văn bản đến
1. **Mở văn bản xem chi tiết:** Dùng chuột nhấp đúp (click liên tục 2 lần) vào dòng văn bản muốn mở trong bảng danh sách. Hệ thống mở ra một tab làm việc mới hiển thị toàn bộ nội dung.
2. **Đọc văn bản trực tiếp:** Nhìn vào mục "Tệp đính kèm" (biểu tượng ghim giấy 📎). Bấm chuột trái trực tiếp vào tên tệp (`.pdf` hoặc `.docx`). Trình duyệt mở tab mới hiển thị nội dung tệp để đọc ngay.
3. **Tải tệp về máy tính:** Bấm vào biểu tượng **tải xuống (⬇️)** nằm bên phải tên tệp đính kèm. Tệp được lưu mặc định trong thư mục **Downloads** trên máy tính.

### 4.5. Cách chuyển tiếp văn bản đến (Chuyển xử lý cho người khác)
1. **Mở tính năng chuyển tiếp:** Tại màn hình xem chi tiết văn bản, nhìn lên thanh công cụ phía trên và bấm nút **"Chuyển xử lý"**.
2. **Chọn người nhận từ danh sách:** Cửa sổ sơ đồ tổ chức (cây đơn vị) hiện lên:
   - Bấm biểu tượng dấu cộng **(+)** hoặc mũi tên nhỏ trước tên phòng ban để mở rộng danh sách nhân viên.
   - Tìm tên người muốn chuyển, tick chọn vào ô vuông trước tên.
   - Chọn vai trò xử lý: **Xử lý chính** (người chịu trách nhiệm giải quyết chính), **Đồng xử lý** (người phối hợp), hoặc **Nhận để biết** (gửi xem thông tin).
3. **Nhập ý kiến chỉ dẫn:** Gõ nội dung yêu cầu xử lý vào khung **"Ý kiến xử lý"** (Ví dụ: "Chuyển đồng chí Nguyễn Văn A xử lý, tham mưu văn bản phúc đáp trước ngày 05/07").
4. **Gửi đi:** Bấm nút **"Gửi"** màu đỏ. Văn bản tự động chuyển đi và biến mất khỏi danh sách "Văn bản chờ xử lý".

**Thu hồi văn bản đã chuyển nhầm:**
- Mở danh sách **"Văn bản đã xử lý"**.
- Nhấp đúp mở văn bản đó.
- Chọn tab **"Xem luân chuyển"** ở góc dưới.
- Bấm nút **"Thu hồi"**.
- **Lưu ý:** Chỉ thu hồi thành công khi người nhận **chưa bấm mở xem** văn bản đó.

### 4.6. Cách hoàn thành văn bản đến (Khi đã giải quyết xong)
1. **Mở văn bản:** Nhấp đúp chuột để mở chi tiết văn bản cần báo cáo hoàn thành.
2. **Bấm nút "Hoàn thành"** trên thanh công cụ phía trên.
3. **Ghi nhận thông tin xử lý:** Nhập tóm tắt kết quả xử lý vào ô ý kiến (Ví dụ: "Đã soạn dự thảo công văn gửi UBND huyện ngày 28/06" hoặc "Đã nghiên cứu và lưu hồ sơ theo dõi").
4. **Xác nhận:** Bấm nút **"Ghi lại"** để lưu. Văn bản chuyển sang trạng thái "Đã hoàn thành".

**Mẹo:** Nếu muốn hoàn thành nhiều văn bản cùng lúc, tại danh sách chờ xử lý, tick chọn vào ô vuông đầu dòng của các văn bản, sau đó bấm nút **"Hoàn thành"** trên thanh công cụ chung.

### 4.7. Văn bản đã xử lý
- Đường dẫn: VĂN BẢN ĐẾN → Văn bản đã xử lý
- Hiển thị tất cả văn bản đã chuyển tiếp hoặc bấm hoàn thành.
- Chức năng hỗ trợ:
  - Xem lại chi tiết, đọc file đính kèm
  - Xem biểu đồ luân chuyển (ai đã xử lý, chuyển tiếp cho ai)
  - Lưu văn bản vào hồ sơ công việc
  - Xuất danh sách ra file Excel để báo cáo

### 4.8. Văn bản bị trả lại
- Đường dẫn: VĂN BẢN ĐẾN → Văn bản đề nghị trả lại
- Văn bản bị người nhận trả lại do không đúng thẩm quyền, sai nội dung...
- Bạn có thể:
  - Đọc **lý do trả lại** của người trả
  - **Chuyển xử lý lại** cho người/đơn vị khác phù hợp hơn
  - Bấm **Hoàn thành** nếu đã tự xử lý xong

---

## 5. MODULE VĂN BẢN ĐI

### 5.1. Tổng quan
Module Văn bản đi quản lý quá trình soạn thảo, ký duyệt và phát hành văn bản do cơ quan ban hành.

**Luồng xử lý chuẩn:**
`Chuyên viên tạo dự thảo → Trình ký Lãnh đạo → Lãnh đạo phê duyệt/Ký số → Văn thư cấp số, đóng dấu số → Ban hành/Gửi đi`

**Các chức năng con:**

| Chức năng con | Ý nghĩa | Đường dẫn menu |
|--------------|---------|---------------|
| Dự thảo của tôi | Các văn bản đang soạn, **chưa trình ký** | VĂN BẢN ĐI → Dự thảo của tôi |
| VB ký duyệt | Văn bản đã trình, đang **chờ lãnh đạo ký** | VĂN BẢN ĐI → Văn bản ký duyệt |
| Tra cứu VB đi | Tìm kiếm toàn bộ VB đi tham gia | VĂN BẢN ĐI → Tra cứu VB đi của tôi |
| Theo dõi VB đi | Xem đơn vị nhận đã **mở đọc chưa** | VĂN BẢN ĐI → Theo dõi văn bản đi |

### 5.2. Tạo dự thảo văn bản đi mới (Dành cho Chuyên viên)
1. **Mở form thêm mới:** Bấm nút **"Thêm mới"** (biểu tượng dấu cộng đỏ) trên thanh công cụ phía trên. Cửa sổ phiếu thông tin dự thảo mở ra.
2. **Điền các thông tin cơ bản** (ô có dấu `*` là bắt buộc):
   - **Sổ văn bản (*):** Chọn tên sổ văn bản đi của đơn vị trong danh sách xổ xuống (Ví dụ: "Sổ văn bản đi Đảng ủy").
   - **Loại văn bản (*):** Chọn thể loại (Công văn, Quyết định, Báo cáo, Kế hoạch...).
   - **Trích yếu (*):** Nhập tóm tắt nội dung chính (Ví dụ: "V/v phối hợp tổ chức Đại hội thể dục thể thao xã năm 2026").
   - **Độ khẩn / Độ mật:** Chọn mức độ khẩn (Thường, Khẩn, Hỏa tốc) hoặc bảo mật nếu có yêu cầu.
3. **Tải tệp đính kèm:** Tại mục "File đính kèm", bấm **"Chọn tập tin"** (hoặc kéo thả tệp từ máy tính). Chọn file dự thảo Word (.docx). Đợi thanh xanh chạy hết 100%.
4. **Lưu dự thảo:** Bấm nút **"Ghi lại"** ở góc trên bên trái. Dự thảo được lưu nhưng chưa gửi cho bất kỳ ai.

> **QUAN TRỌNG:** Tuyệt đối **KHÔNG** tự ý bấm nút "Phát hành" nếu chưa được phân quyền hoặc chưa có ý kiến phê duyệt của Lãnh đạo. Đối với Chuyên viên, chỉ thực hiện Trình ký nội bộ.

### 5.3. Trình ký lên Lãnh đạo phê duyệt
1. **Mở dự thảo đã lưu:** Nhấp đúp mở dự thảo vừa tạo từ danh sách.
2. **Mở luồng ký duyệt:** Bấm nút **"Trình ký"** trên thanh công cụ phía trên.
3. **Chọn người ký:**
   - Chọn Lãnh đạo **ký chính** (Ví dụ: Bí thư/Phó Bí thư tương ứng).
   - Chọn người **kiểm tra ký nháy** (nếu có yêu cầu từ đơn vị).
4. **Gửi đi:** Bấm nút **"Gửi"**. Dự thảo chuyển trạng thái sang "Đang chờ ký" và nằm trong mục "Văn bản ký duyệt".

### 5.4. Theo dõi văn bản ký duyệt
- Đường dẫn: VĂN BẢN ĐI → Văn bản ký duyệt
- Theo dõi các trạng thái: **Đang chờ ký**, **Đã ký**, **Bị trả lại**
- Khi văn bản bị trả lại, chuyên viên cần mở lại dự thảo, sửa theo ý kiến của lãnh đạo rồi trình ký lại.

### 5.5. Theo dõi văn bản đi
- Đường dẫn: VĂN BẢN ĐI → Theo dõi văn bản đi
- Xem trạng thái: ai đã nhận, ai chưa nhận văn bản đi.
- Rất hữu ích để kiểm tra đơn vị nhận đã tiếp nhận chưa.

---

## 6. MODULE PHIẾU TRÌNH

### 6.1. Tổng quan
Phiếu trình dùng để đề xuất ý kiến, phương án xử lý công việc trực tiếp lên cấp trên mà không cần qua luồng văn bản đi phức tạp.

**Các chức năng con:**

| Chức năng | Ý nghĩa | Đường dẫn menu |
|-----------|---------|---------------|
| PT của tôi | Phiếu trình bạn đã tạo | PHIẾU TRÌNH → Phiếu trình của tôi |
| PT cần phê duyệt | Phiếu trình người khác gửi cho bạn duyệt | PHIẾU TRÌNH → Phiếu trình cần phê duyệt |
| PT nhận để biết | Phiếu trình gửi cho bạn để nắm thông tin | PHIẾU TRÌNH → Phiếu trình nhận để biết |

### 6.2. Tạo phiếu trình xin ý kiến Lãnh đạo
1. **Mở phiếu mới:** Bấm **"Thêm mới"** (biểu tượng dấu cộng đỏ) trên thanh công cụ.
2. **Điền trích yếu đề xuất (*):** Nhập tóm tắt vấn đề cần xin ý kiến (Ví dụ: "Tờ trình đề xuất phương án mua sắm trang thiết bị phòng họp cơ quan năm 2026").
3. **Nhập ý kiến đề xuất chi tiết:** Gõ nội dung đề xuất cụ thể hoặc các phương án đề nghị Lãnh đạo xem xét.
4. **Tải tài liệu đính kèm:** Bấm **"Chọn tập tin"** để tải lên tài liệu Word, Excel hoặc bản dự toán chi tiết. Đợi thanh xanh chạy hết 100%.
5. **Lưu phiếu trình:** Bấm **"Ghi lại"** ở góc trên bên trái.
6. **Trình Lãnh đạo phê duyệt:**
   - Bấm nút **"Trình xin ý kiến"** trên thanh công cụ.
   - Tại ô Tìm kiếm nhanh, gõ tên Lãnh đạo cần trình.
   - Chọn đúng đồng chí Lãnh đạo (tick ô vuông trước tên).
   - Tại ô vai trò, tick chọn **"Ký chính"**.
   - Bấm nút **"Gửi"** màu đỏ.

**Hủy/Rút phiếu trình đã gửi:**
- Nhấp đúp vào phiếu trình trong danh sách.
- Bấm nút **"Hủy luồng xin ý kiến"** trên thanh công cụ.
- **Lưu ý:** Chỉ thực hiện được khi Lãnh đạo **chưa bấm duyệt** phiếu trình.

### 6.3. Phiếu trình cần phê duyệt (Dành cho Lãnh đạo)
- Đường dẫn: PHIẾU TRÌNH → Phiếu trình cần phê duyệt
- Danh sách phiếu trình người khác gửi cho bạn.
- Lãnh đạo có thể: **Đồng ý**, **Cho ý kiến**, **Trả lại**.

### 6.4. Phiếu trình nhận để biết
- Đường dẫn: PHIẾU TRÌNH → Phiếu trình nhận để biết
- Phiếu trình gửi cho bạn với mục đích **để biết/theo dõi thông tin**, không yêu cầu phê duyệt.
- Có thể:
  - **Xem chi tiết nội dung:** Nhấp đúp để xem nội dung đề xuất, tài liệu đính kèm và ý kiến đóng góp.
  - **Theo dõi tiến độ/Luồng xử lý:** Chọn tab **"Xem luồng xử lý"** để biết phiếu trình đang gửi đến ai, lãnh đạo nào đã cho ý kiến.
  - **Tải tài liệu đính kèm** để phục vụ phối hợp chuyên môn.

---

## 7. MODULE QUẢN LÝ NHIỆM VỤ

### 7.1. Tổng quan
Chức năng Quản lý nhiệm vụ giúp số hóa các chỉ đạo của lãnh đạo thành các đầu việc có thời hạn cụ thể, cho phép chuyên viên theo dõi sát sao các công việc được giao.

- Đường dẫn: QUẢN LÝ NHIỆM VỤ → Danh sách nhiệm vụ

### 7.2. Xem và lọc danh sách nhiệm vụ
Bộ lọc ở góc trên màn hình danh sách:

| Bộ lọc | Ý nghĩa |
|--------|---------|
| Nhiệm vụ cá nhân | Chỉ hiện các việc được giao cho riêng bạn |
| Nhiệm vụ phối hợp | Các công việc bạn tham gia với vai trò hỗ trợ |
| Nhiệm vụ giao đi | Các công việc do bạn tạo và giao cho người khác |
| Lọc theo trạng thái | Chưa thực hiện, Đang thực hiện, Hoàn thành, Hoàn thành quá hạn, Quá hạn |

### 7.3. Báo cáo tiến độ và hoàn thành nhiệm vụ
1. **Mở chi tiết nhiệm vụ:** Nhấp đúp vào dòng nhiệm vụ cần báo cáo.
2. **Bấm nút "Cập nhật tiến độ"** trên thanh công cụ (hoặc chọn tab "Báo cáo tiến độ" bên dưới).
3. **Nhập thông tin:**
   - **% hoàn thành:** Nhập số phần trăm tiến độ thực tế (50%, 80%, 100%...).
   - **Nội dung báo cáo:** Viết chi tiết phần việc đã làm, kết quả đạt được, khó khăn vướng mắc (nếu có).
   - **Tài liệu đính kèm:** Chọn file báo cáo/sản phẩm công việc từ máy tính tải lên làm minh chứng.
4. **Ghi lại:** Bấm **"Ghi lại"** để lưu. Nếu nhập 100%, nhiệm vụ tự động chuyển sang trạng thái *Chờ xác nhận hoàn thành* từ phía Lãnh đạo.
* **Quy tắc trễ hạn:** Trường hợp nhiệm vụ được hoàn thành 100% nhưng trễ hơn so với ngày đến hạn đã được giao, hệ thống sẽ tự động cập nhật trạng thái của nhiệm vụ đó thành **"Hoàn thành quá hạn"**.

### 7.4. Trao đổi và thảo luận công việc
1. Nhấp đúp vào nhiệm vụ → chọn tab **"Thảo luận"** ở góc dưới.
2. Nhập nội dung ý kiến, giải trình hoặc câu hỏi trao đổi.
3. Bấm **"Gửi"**. Nội dung hiển thị theo dòng thời gian và thông báo đến Lãnh đạo ngay lập tức.

### 7.5. Tự tạo nhiệm vụ / Giao việc
1. Bấm nút **"Thêm mới"** trên thanh công cụ.
2. Điền đầy đủ: **Tên nhiệm vụ (*)**, Nội dung chi tiết, Ngày bắt đầu, Hạn hoàn thành.
3. Tại phần **Người thực hiện**, gõ tên cán bộ cần giao việc.
4. Bấm **"Ghi lại"** để khởi tạo nhiệm vụ.

### 7.6. Báo cáo đơn vị
- Tổng hợp tiến độ công việc định kỳ của phòng ban.
- Giúp lãnh đạo có cái nhìn tổng quan về hiệu suất làm việc.

---

## 8. MODULE LỊCH HỌP

### 8.1. Tổng quan
Chức năng Lịch họp cung cấp toàn bộ lịch công tác, lịch họp tập trung của cơ quan.

### 8.2. Lịch tuần cơ quan
- Đường dẫn: LỊCH HỌP → Lịch tuần cơ quan
- Hiển thị dạng bảng phân chia theo từng ngày trong tuần (Thứ Hai → Chủ Nhật) và theo buổi (Sáng/Chiều).
- Thông tin hiển thị: Thời gian bắt đầu, tiêu đề cuộc họp, thành phần tham dự, địa điểm/phòng họp, người chủ trì.

### 8.3. Xem chi tiết cuộc họp và tải tài liệu
1. **Chọn cuộc họp:** Di chuột đến cuộc họp trên bảng lịch tuần và nhấp đúp.
2. **Kiểm tra tài liệu:** Nhìn xuống mục **"Tài liệu đính kèm"** phía dưới.
3. **Tải file:** Bấm trực tiếp vào tên tệp đính kèm (.pdf, .docx, .xlsx...) để tải về.

### 8.4. Kết xuất lịch tuần ra Word để in
1. Mở màn hình Lịch tuần cơ quan.
2. Bấm nút biểu tượng **Tải xuống (📥 - Xuất Word)** ở thanh công cụ phía trên bên phải.
3. Hệ thống tự động xuất lịch tuần hiện tại ra file Word (.docx) có định dạng bảng biểu chuẩn công vụ. Mở file lên và nhấn in.

### 8.5. Lịch tuần lãnh đạo
- Hiển thị lịch công tác riêng của các đồng chí Thường trực Đảng ủy/Lãnh đạo đơn vị.

### 8.6. Quy tắc khi tạo lịch họp mới (Dành cho Quản trị viên/Văn thư phụ trách)
* **Thời lượng mặc định:** Khi khởi tạo cuộc họp mới, hệ thống sẽ tự động gán thời lượng mặc định của cuộc họp là **1 giờ**. Nếu cuộc họp kéo dài hơn, người tạo lịch cần chủ động chỉnh sửa lại thời gian kết thúc.
* **Người chủ trì bắt buộc:** Mỗi cuộc họp được tạo trên hệ thống **bắt buộc** phải cấu hình trường **Người chủ trì** (Host - Ví dụ: Bí thư, Phó Bí thư, Chánh văn phòng, v.v.). Nếu để trống trường này, hệ thống sẽ chặn không cho lưu cuộc họp.

---

## 9. MODULE QUẢN LÝ HỒ SƠ

### 9.1. Tổng quan
Gom nhóm các văn bản đến, văn bản đi và phiếu trình có liên quan vào một hồ sơ vụ việc chung để quản lý logic.

### 9.2. Chức năng chính
- **Tạo hồ sơ mới:** Tạo thư mục hồ sơ theo vụ việc, dự án hoặc chủ đề.
- **Thêm văn bản vào hồ sơ:** Khi xem chi tiết văn bản đến/đi/phiếu trình, chọn lưu vào hồ sơ tương ứng.
- **Bàn giao hồ sơ:** Chuyển quyền sở hữu hồ sơ cho người khác (ví dụ: khi chuyển công tác, nghỉ phép dài ngày).
- **Chia sẻ hồ sơ:** Cho phép người khác xem hồ sơ (chỉ quyền xem, không sửa/xóa).

### 9.3. Quy tắc lưu trữ hồ sơ tài liệu
* **Đếm số trang khi tải lên:** Khi người dùng quét (scan) từ tài liệu giấy hoặc tải lên các file đính kèm để lưu trữ vào hồ sơ công việc, bắt buộc phải đếm và điền số lượng trang thực tế của từng tài liệu đính kèm.
* **Tổng số trang bắt buộc khi kết thúc hồ sơ:** Khi hoàn thành/đóng luồng hoặc thực hiện lưu trữ chính thức ("kết thúc") hồ sơ, hệ thống yêu cầu **bắt buộc phải có Tổng số trang tài liệu** trong hồ sơ. Nếu thiếu thông tin này, hệ thống sẽ báo lỗi và chặn không cho hoàn tất thủ tục lưu trữ/kết thúc hồ sơ.

---

## 10. MODULE TÀI LIỆU CÁ NHÂN

### 10.1. Tổng quan
Giống như một thư viện lưu trữ cá nhân trên Cloud. Mỗi người dùng có thể tạo danh mục thư mục riêng.

### 10.2. Cách sử dụng
- **Tạo danh mục thư mục:** Tạo cấu trúc thư mục cá nhân để phân loại tài liệu.
- **Lưu tài liệu từ hệ thống:** Khi xem bất kỳ văn bản nào trên hệ thống, bấm **"Lưu tài liệu cá nhân"** để sao chép về kho cá nhân.
- **Tải tài liệu từ máy tính:** Tải lên các file từ máy tính cá nhân để lưu trữ.

---

## 11. MODULE VĂN BẢN CÔNG KHAI

### 11.1. Tổng quan
Cho phép tra cứu các văn bản được công khai trong hệ thống — các văn bản mà tất cả người dùng trong đơn vị đều có thể xem.

### 11.2. Chức năng
- Tìm kiếm văn bản công khai theo số ký hiệu, trích yếu, cơ quan ban hành...
- Đọc và tải file văn bản công khai.
- Không cần được phân phối trực tiếp mới xem được.

---

## 12. MODULE THEO DÕI KPI

### 12.1. Tổng quan
Chức năng Theo dõi KPI (Key Performance Indicator) giúp đánh giá hiệu suất làm việc của cá nhân và đơn vị dựa trên các chỉ số đo lường cụ thể.

### 12.2. Chức năng
- Xem bảng KPI cá nhân theo kỳ.
- Theo dõi các chỉ số: số văn bản xử lý đúng hạn, số nhiệm vụ hoàn thành, tỷ lệ quá hạn...
- Báo cáo tổng hợp KPI đơn vị.

---

## 13. MODULE QUẢN TRỊ HỆ THỐNG

### 13.1. Tổng quan
Dành cho quản trị viên (Admin) hệ thống. Người dùng thông thường không có quyền truy cập module này.

### 13.2. Chức năng chính
- **Quản lý danh mục:** Thêm/sửa/xóa các danh mục dùng chung (loại văn bản, sổ văn bản, đơn vị, chức vụ...).
- **Quản lý người dùng:** Tạo tài khoản, phân quyền, reset mật khẩu.
- **Quản lý đơn vị/phòng ban:** Cập nhật cơ cấu tổ chức, sơ đồ cây đơn vị.
- **Quản lý sổ văn bản:** Tạo và quản lý các sổ văn bản đến/đi của đơn vị.
- **Cấu hình hệ thống:** Thiết lập các thông số vận hành.

### 13.3. Quy tắc cấu hình chữ ký số và con dấu đơn vị
* **Ảnh chữ ký Lãnh đạo:** Khi tải lên ảnh chữ ký số cá nhân cho Lãnh đạo (có thể thực hiện bởi Admin hoặc chính người dùng trong trang thông tin cá nhân), ảnh chữ ký phải được cắt sát, định dạng **PNG** và **bắt buộc phải xóa hoàn toàn nền trắng (nền trong suốt)**.
* **Ảnh con dấu đơn vị (Unit symbol):** Khi cấu hình ảnh con dấu tròn của đơn vị, chiều cao (Height) của ảnh phải được thiết lập là **110**.
* **Ảnh dấu chỉ đạo/xác nhận phụ (Confirmation symbol):** Chiều rộng (Width) của ảnh dấu được hệ thống khuyến nghị đặt là **680** (kích thước tối ưu giúp hiển thị cân đối và khớp chính xác nhất với mẫu văn bản giấy và chữ ký).
* **Quyền quản lý hình ảnh dấu/logo:** Cả **Quản trị viên hệ thống (Admin)** và cán bộ **Văn thư (Clerk)** đều có thẩm quyền cập nhật, quản lý và chỉnh sửa danh mục hình ảnh con dấu/logo của đơn vị.

---

## 14. XỬ LÝ SỰ CỐ THƯỜNG GẶP

### 14.1. Hệ thống bị đơ / Không load dữ liệu
- **Giải pháp:** Sử dụng tổ hợp phím `Ctrl + F5` để làm mới hoàn toàn bộ nhớ cache của trình duyệt.
- Nếu vẫn không khắc phục, thử đóng trình duyệt và mở lại.

### 14.2. Lỗi hiển thị giao diện / Bảng biểu
- **Giải pháp:** Luôn sử dụng **Google Chrome** hoặc **Microsoft Edge** phiên bản mới nhất. Các trình duyệt khác (Firefox, Safari) có thể gây lỗi hiển thị bảng biểu ZK.

### 14.3. Không đăng nhập được
- Kiểm tra lại tên đăng nhập và mật khẩu (phân biệt chữ HOA/thường).
- Bấm biểu tượng 👁 bên phải ô mật khẩu để kiểm tra mật khẩu đã gõ đúng chưa.
- Nếu quên mật khẩu, bấm **"Quên mật khẩu"** hoặc liên hệ quản trị viên.

### 14.4. Không tải được file đính kèm
- Kiểm tra kết nối internet.
- Thử bấm chuột phải vào tên file → "Lưu liên kết thành..." (Save Link As...) để tải trực tiếp.
- Kiểm tra trình duyệt có chặn popup không.

### 14.5. Văn bản chuyển nhầm người
- Mở danh sách **"Văn bản đã xử lý"**.
- Nhấp đúp mở văn bản.
- Chọn tab **"Xem luân chuyển"** → bấm **"Thu hồi"**.
- **Lưu ý:** Chỉ thu hồi thành công khi người nhận chưa mở xem.

### 14.6. Phiếu trình gửi nhầm / cần sửa đổi
- Nhấp đúp vào phiếu trình trong danh sách.
- Bấm nút **"Hủy luồng xin ý kiến"**.
- Chỉ thực hiện được khi Lãnh đạo chưa phê duyệt.

---

## 15. QUY TẮC AN TOÀN VÀ BẢO MẬT

### 15.1. Quy tắc bắt buộc
1. **Tuyệt đối không tự ý phát hành** hoặc gửi bất kỳ văn bản thử nghiệm/văn bản nháp nào ra các cơ quan, đơn vị khác ngoài hệ thống.
2. Các văn bản đi **bắt buộc** phải đi qua luồng duyệt và ký số hợp lệ của người có thẩm quyền trước khi Văn thư phát hành.
3. Tuyệt đối **bảo mật tài khoản đăng nhập** cá nhân.
4. Thực hiện **đăng xuất ngay** sau khi kết thúc phiên làm việc trên các máy tính dùng chung.
5. **Không chia sẻ** mật khẩu cho bất kỳ ai.

### 15.2. Khuyến nghị
- Đổi mật khẩu định kỳ (khuyến nghị 3 tháng/lần).
- Sử dụng mật khẩu mạnh (tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt).
- Không lưu mật khẩu trên trình duyệt của máy tính dùng chung.

---

## 16. CÂU HỎI THƯỜNG GẶP (FAQ)

### Đăng nhập & Tài khoản

**H: Tôi truy cập hệ thống ở đâu?**
Đ: Truy cập tại địa chỉ https://dhtn.dcs.vn bằng trình duyệt Google Chrome hoặc Microsoft Edge.

**H: Tôi quên mật khẩu, phải làm sao?**
Đ: Bấm vào chữ "Quên mật khẩu" trên màn hình đăng nhập. Hoặc liên hệ trực tiếp quản trị viên hệ thống để được reset mật khẩu.

**H: Tôi có thể đăng nhập bằng VNeID không?**
Đ: Có. Bạn có thể đăng nhập bằng VNeID qua nút phía dưới màn hình đăng nhập. Liên hệ bộ phận IT để được hướng dẫn kích hoạt.

**H: Làm sao để đăng xuất?**
Đ: Bấm vào tên của bạn ở góc trên bên phải → chọn "Đăng xuất".

**H: Tôi có thể đổi mật khẩu không?**
Đ: Có. Bấm vào tên của bạn ở góc trên bên phải → chọn "Đổi mật khẩu".

---

### Văn bản đến

**H: Làm sao để xem văn bản mới chuyển đến cho tôi?**
Đ: Vào menu bên trái → VĂN BẢN ĐẾN → Văn bản chờ xử lý. Đây là danh sách tất cả văn bản mới được chuyển đến cho bạn mà chưa xử lý xong.

**H: Làm sao để mở xem chi tiết một văn bản?**
Đ: Nhấp đúp chuột (click liên tục 2 lần) vào dòng văn bản trong bảng danh sách.

**H: Làm sao để tải file văn bản về máy?**
Đ: Mở chi tiết văn bản, tìm mục "Tệp đính kèm" (📎). Bấm biểu tượng tải xuống (⬇️) bên phải tên tệp. File sẽ được lưu trong thư mục Downloads.

**H: Làm sao để đọc file mà không cần tải về?**
Đ: Bấm chuột trái trực tiếp vào tên tệp đính kèm (.pdf hoặc .docx). Trình duyệt sẽ mở tab mới hiển thị nội dung.

**H: Tôi muốn chuyển văn bản cho người khác xử lý thì làm sao?**
Đ: Mở chi tiết văn bản → bấm nút "Chuyển xử lý" trên thanh công cụ → chọn người nhận trong sơ đồ tổ chức → tick vai trò (Xử lý chính/Đồng xử lý/Nhận để biết) → nhập ý kiến → bấm "Gửi".

**H: Tôi chuyển văn bản nhầm người, làm sao thu hồi?**
Đ: Mở danh sách "Văn bản đã xử lý" → nhấp đúp mở văn bản → chọn tab "Xem luân chuyển" → bấm "Thu hồi". Lưu ý: Chỉ thu hồi được khi người nhận chưa mở xem văn bản.

**H: Khi nào thì bấm "Hoàn thành" văn bản?**
Đ: Khi bạn đã giải quyết xong nội dung công việc liên quan đến văn bản đó. Mở văn bản → bấm "Hoàn thành" → nhập tóm tắt kết quả → bấm "Ghi lại".

**H: Có thể hoàn thành nhiều văn bản cùng lúc không?**
Đ: Có. Tại danh sách chờ xử lý, tick chọn vào ô vuông đầu dòng của các văn bản cần hoàn thành, sau đó bấm nút "Hoàn thành" trên thanh công cụ chung.

**H: Làm sao tìm lại một văn bản cũ từ nhiều tháng trước?**
Đ: Sử dụng chức năng "Tra cứu VB đến tôi" (VĂN BẢN ĐẾN → Tra cứu VB đến tôi). Đây là công cụ tìm kiếm mạnh nhất, cho phép lọc theo Số đến, Số ký hiệu, Ngày văn bản, Cơ quan ban hành, Độ khẩn/mật, Trạng thái xử lý...

**H: "Văn bản nhận để biết" là gì? Tôi có cần xử lý không?**
Đ: Đây là văn bản gửi cho bạn chỉ để nắm thông tin. Bạn KHÔNG cần xử lý hay hoàn thành — chỉ cần đọc để biết.

**H: Tại sao văn bản bị trả lại?**
Đ: Văn bản bị người nhận trả lại do không đúng thẩm quyền, sai nội dung hoặc lý do khác. Bạn có thể đọc lý do trả lại, sau đó chuyển xử lý cho người khác hoặc tự xử lý rồi bấm hoàn thành.

---

### Văn bản đi

**H: Tôi muốn soạn văn bản đi mới thì làm sao?**
Đ: Vào VĂN BẢN ĐI → Dự thảo của tôi → bấm "Thêm mới" → điền thông tin (Sổ VB, Loại VB, Trích yếu) → tải file dự thảo .docx → bấm "Ghi lại" để lưu.

**H: Làm sao gửi dự thảo lên Lãnh đạo ký?**
Đ: Mở dự thảo đã lưu → bấm "Trình ký" → chọn Lãnh đạo ký chính và người kiểm tra ký nháy (nếu có) → bấm "Gửi".

**H: Chuyên viên có thể tự phát hành văn bản không?**
Đ: KHÔNG. Chuyên viên chỉ soạn dự thảo và trình ký. Việc cấp số, đóng dấu và phát hành là nhiệm vụ của Văn thư, sau khi đã có chữ ký số hợp lệ của Lãnh đạo.

**H: Làm sao biết đơn vị nhận đã đọc văn bản đi chưa?**
Đ: Vào VĂN BẢN ĐI → Theo dõi văn bản đi. Bạn sẽ thấy trạng thái tiếp nhận của từng đơn vị: đã nhận hay chưa nhận.

**H: Dự thảo bị Lãnh đạo trả lại thì phải làm sao?**
Đ: Mở dự thảo trong mục "Văn bản ký duyệt" → đọc ý kiến trả lại của Lãnh đạo → sửa đổi nội dung theo yêu cầu → trình ký lại.

**H: Kích thước ảnh chữ ký chuẩn trên hệ thống ĐHTN là bao nhiêu?**
Đ: Kích thước ảnh chữ ký trên hệ thống ĐHTN là **480x110** pixels, sử dụng **cỡ chữ 10**.

---

### Phiếu trình

**H: Phiếu trình khác gì văn bản đi?**
Đ: Phiếu trình dùng để đề xuất ý kiến, xin chủ trương trực tiếp lên cấp trên về công việc phát sinh — nội bộ đơn vị, không cần cấp số phát hành ra bên ngoài. Văn bản đi là văn bản chính thức, có cấp số, đóng dấu và gửi ra cơ quan bên ngoài.

**H: Tôi muốn rút lại phiếu trình đã gửi thì làm sao?**
Đ: Nhấp đúp vào phiếu trình trong danh sách → bấm "Hủy luồng xin ý kiến". Chỉ thực hiện được khi Lãnh đạo chưa phê duyệt.

---

### Nhiệm vụ

**H: Làm sao xem danh sách nhiệm vụ được giao cho tôi?**
Đ: Vào QUẢN LÝ NHIỆM VỤ → Danh sách nhiệm vụ → chọn bộ lọc "Nhiệm vụ cá nhân" ở góc trên.

**H: Làm sao báo cáo tiến độ nhiệm vụ?**
Đ: Nhấp đúp vào nhiệm vụ → bấm "Cập nhật tiến độ" → nhập % hoàn thành + nội dung báo cáo + file đính kèm → bấm "Ghi lại". Nếu nhập 100%, nhiệm vụ tự động chuyển sang "Chờ xác nhận hoàn thành".

**H: Tôi có thể trao đổi trực tiếp với người giao việc trên hệ thống không?**
Đ: Có. Nhấp đúp vào nhiệm vụ → chọn tab "Thảo luận" → nhập nội dung → bấm "Gửi". Nội dung sẽ hiển thị theo dòng thời gian và thông báo cho Lãnh đạo.

**H: Tôi có thể tự tạo nhiệm vụ và giao cho người khác không?**
Đ: Có. Bấm "Thêm mới" trên thanh công cụ → điền Tên nhiệm vụ, Nội dung, Ngày bắt đầu, Hạn hoàn thành → chọn Người thực hiện → bấm "Ghi lại".

---

### Lịch họp

**H: Xem lịch họp ở đâu?**
Đ: Vào LỊCH HỌP → Lịch tuần cơ quan. Giao diện bảng phân chia theo ngày (Thứ Hai → Chủ Nhật) và theo buổi (Sáng/Chiều).

**H: Làm sao tải tài liệu chuẩn bị cuộc họp?**
Đ: Trên bảng lịch tuần, nhấp đúp vào cuộc họp → nhìn xuống mục "Tài liệu đính kèm" → bấm vào tên tệp để tải về.

**H: Có thể in lịch tuần ra giấy không?**
Đ: Có. Mở Lịch tuần cơ quan → bấm nút "Xuất Word" (📥) trên thanh công cụ. Hệ thống xuất ra file Word (.docx) có định dạng chuẩn công vụ. Mở file và in.

---

### Hồ sơ & Tài liệu

**H: Hồ sơ dùng để làm gì?**
Đ: Hồ sơ giúp gom nhóm các văn bản đến, văn bản đi và phiếu trình liên quan vào một vụ việc chung để dễ quản lý. Ví dụ: Tạo hồ sơ "Đại hội Đảng bộ nhiệm kỳ 2025-2030" và lưu tất cả văn bản liên quan vào đó.

**H: Tôi có thể chia sẻ hồ sơ cho đồng nghiệp không?**
Đ: Có. Hệ thống hỗ trợ 2 cách: "Bàn giao hồ sơ" (chuyển quyền sở hữu) và "Chia sẻ hồ sơ" (chỉ cho phép xem, không sửa/xóa).

**H: Tài liệu cá nhân là gì?**
Đ: Đó là thư viện lưu trữ cá nhân trên Cloud. Bạn có thể tạo danh mục thư mục riêng và lưu bất kỳ văn bản nào trên hệ thống vào đây bằng nút "Lưu tài liệu cá nhân".

---

### Sự cố kỹ thuật

**H: Hệ thống bị đơ, không load dữ liệu thì phải làm sao?**
Đ: Nhấn tổ hợp phím `Ctrl + F5` để làm mới hoàn toàn bộ nhớ cache trình duyệt. Nếu vẫn không được, đóng hoàn toàn trình duyệt rồi mở lại.

**H: Giao diện bị lỗi hiển thị, các bảng biểu không đúng thì sao?**
Đ: Luôn sử dụng Google Chrome hoặc Microsoft Edge phiên bản mới nhất. Các trình duyệt khác có thể không tương thích hoàn toàn với ZK Framework.

**H: Không tải được file đính kèm?**
Đ: Kiểm tra kết nối internet. Thử bấm chuột phải vào tên file → "Lưu liên kết thành..." (Save Link As...) để tải trực tiếp. Hoặc kiểm tra trình duyệt có đang chặn popup không.

**H: Upload file dự thảo bị lỗi?**
Đ: Kiểm tra dung lượng file (không quá lớn). Đảm bảo file đúng định dạng (.docx, .pdf, .xlsx). Đợi thanh xanh chạy hết 100% trước khi thực hiện thao tác tiếp theo.

---

## PHỤ LỤC: BẢNG TÓM TẮT PHÍM TẮT VÀ THAO TÁC NHANH

| Thao tác | Cách thực hiện |
|----------|---------------|
| Mở chi tiết văn bản/phiếu trình/nhiệm vụ | Nhấp đúp chuột vào dòng trong danh sách |
| Làm mới trang khi bị đơ | `Ctrl + F5` |
| Thêm mới dự thảo/phiếu trình/nhiệm vụ | Bấm nút "Thêm mới" (dấu cộng đỏ) trên thanh công cụ |
| Lưu thông tin đã nhập | Bấm nút "Ghi lại" |
| Chuyển văn bản cho người khác | Bấm "Chuyển xử lý" → chọn người → "Gửi" |
| Thu hồi văn bản đã chuyển nhầm | Mở VB đã xử lý → Xem luân chuyển → "Thu hồi" |
| Hoàn thành văn bản | Bấm "Hoàn thành" → nhập kết quả → "Ghi lại" |
| Trình ký dự thảo | Mở dự thảo → "Trình ký" → chọn người ký → "Gửi" |
| Trình phiếu trình | Mở phiếu → "Trình xin ý kiến" → chọn Lãnh đạo → "Gửi" |
| Rút phiếu trình | Mở phiếu → "Hủy luồng xin ý kiến" |
| Báo cáo tiến độ nhiệm vụ | Mở nhiệm vụ → "Cập nhật tiến độ" → nhập % + nội dung → "Ghi lại" |
| Đăng xuất | Bấm tên người dùng góc trên phải → "Đăng xuất" |
| Xuất lịch tuần ra Word | Mở Lịch tuần → bấm biểu tượng "Xuất Word" (📥) |

---

## PHỤ LỤC: THUẬT NGỮ CHUYÊN MÔN

| Thuật ngữ | Giải thích |
|-----------|-----------|
| **Văn bản đến** | Văn bản do cơ quan khác gửi đến đơn vị của bạn |
| **Văn bản đi** | Văn bản do đơn vị bạn soạn thảo, ký phát hành gửi ra ngoài |
| **Phiếu trình** | Tờ trình nội bộ để đề xuất ý kiến, xin chủ trương lãnh đạo |
| **Trích yếu** | Nội dung tóm tắt ngắn gọn của văn bản |
| **Bút phê** | Ý kiến chỉ đạo của Lãnh đạo ghi trực tiếp trên văn bản |
| **Luân chuyển** | Quá trình chuyển văn bản qua nhiều người/đơn vị xử lý |
| **Ký số / Chữ ký số** | Chữ ký điện tử có giá trị pháp lý tương đương chữ ký tay (kích thước ảnh chữ ký trên hệ thống ĐHTN là **480x110**, cỡ chữ **10**) |
| **Dự thảo** | Bản soạn thảo ban đầu của văn bản, chưa được ký duyệt chính thức |
| **Sổ văn bản** | Sổ ghi chép, theo dõi, đánh số thứ tự tất cả văn bản đến/đi |
| **Xử lý chính** | Người chịu trách nhiệm chính giải quyết văn bản/công việc |
| **Đồng xử lý** | Người phối hợp thực hiện cùng người xử lý chính |
| **Nhận để biết** | Người nhận bản sao để nắm thông tin, không cần xử lý |
| **Cấp số** | Hành động gán số thứ tự chính thức cho văn bản đi trước khi phát hành |
| **Phát hành** | Gửi văn bản đi chính thức ra các cơ quan, đơn vị bên ngoài |
| **KPI** | Chỉ số đánh giá hiệu suất công việc (Key Performance Indicator) |
| **VNeID** | Ứng dụng định danh điện tử quốc gia của Việt Nam |
| **ZK Framework** | Nền tảng công nghệ web Java dùng để xây dựng giao diện hệ thống |

---

*Tài liệu này được tạo tự động từ hệ thống hướng dẫn sử dụng chính thức và khảo sát thực tế giao diện hệ thống Điều hành tác nghiệp (dhtn.dcs.vn). Mọi thông tin trong tài liệu phản ánh đúng các chức năng và luồng xử lý thực tế tại thời điểm cập nhật.*

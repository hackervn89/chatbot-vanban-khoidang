# Kỹ năng Tạo Văn Bản Khối Đảng (taovanban_khoidang)

---
name: cong-van-giao-viec-generator
description: Kích hoạt khi người dùng cung cấp văn bản chỉ đạo của cấp trên và yêu cầu tạo "Công văn giao việc" của Đảng ủy xã cho các cơ quan, đơn vị cấp dưới triển khai thực hiện. Kỹ năng này sẽ phân tích văn bản cấp trên, tự động trích xuất các thông tin cần thiết, xác định cơ quan chịu trách nhiệm và sử dụng mẫu Công văn chuẩn của Đảng để tạo ra tệp Word (.docx).
---

## 🎯 Mục tiêu & Vai trò
Bạn là một chuyên viên tham mưu và văn thư xuất sắc trực thuộc Đảng ủy xã. Nhiệm vụ của bạn là tiếp nhận các văn bản kế hoạch, quy định, chỉ thị của cấp trên (Tỉnh ủy, Huyện ủy, Trung ương), trích xuất chính xác các thuộc tính pháp lý và phân bổ công việc về cho các ban ngành xã dựa trên đúng chức năng, nhiệm vụ của từng đơn vị.

---

## 🔍 Quy tắc nghiệp vụ (Business Rules)

### 1. Phân tích Văn bản Cấp trên & Xác định Cơ quan ban hành
Để điền vào biến `{{van_ban_cap_tren}}`, bạn cần xây dựng chuỗi văn bản theo chuẩn định dạng hành chính:
`[Thể loại văn bản] số [Ký hiệu], ngày [ngày/tháng/năm] của [Cơ quan ban hành] về [Trích yếu nội dung]`

* **Phiên bản rút gọn (`{{van_ban_cap_tren_rut_gon}}`)**:
  * Định dạng: `[Thể loại văn bản] số [Ký hiệu], ngày [ngày/tháng/năm]` (Ví dụ: *Kế hoạch số 84-KH/TU, ngày 15/6/2026*).
  * Ứng dụng: Được tự động sử dụng trong các **đoạn văn giao việc cụ thể** ở phần thân công văn để tránh lặp đi lặp lại nội dung trích yếu quá dài dòng (do đoạn mở đầu đã ghi đầy đủ thông tin).


Để xác định **Cơ quan ban hành** chính xác (ví dụ để đưa vào cụm *"của [Cơ quan ban hành]"* trong chuỗi `{{van_ban_cap_tren}}` hoặc `{{TRICH_YEU_CONG_VAN}}`):
* **Nguyên tắc xác định:** Đọc kỹ đoạn mở đầu (thường ở câu gần cuối của đoạn mở đầu trước phần nội dung chính) để xem cơ quan nào ban hành, yêu cầu hoặc đề nghị triển khai. Không ghép thêm tên địa phương/tỉnh (như Khánh Hòa, Lâm Đồng,...) vào tên cơ quan ban hành trong chuỗi nội dung văn bản.
* **Cách khớp chi tiết chủ thể:**
  * Nếu văn bản ghi: *"Ban Thường vụ Tỉnh ủy ban hành Kế hoạch..."* $\rightarrow$ Cơ quan ban hành là **Ban Thường vụ Tỉnh ủy**.
  * Nếu văn bản ghi: *"Thường trực Tỉnh ủy chỉ đạo/yêu cầu/đề nghị..."* $\rightarrow$ Cơ quan ban hành là **Thường trực Tỉnh ủy**.
  * Nếu văn bản ghi: *"Tỉnh ủy ban hành..."* hoặc *"Ban Chấp hành Tỉnh ủy ban hành..."* $\rightarrow$ Cơ quan ban hành là **Tỉnh ủy**.

* Việc xác định chính xác này giúp tôn trọng thẩm quyền chỉ đạo và thể thức văn bản hành chính Đảng.

### 2. Phân vai giao việc theo chức năng 5 cơ quan cấp xã

Nếu văn bản chỉ đạo của cấp trên không chỉ rõ đơn vị cụ thể ở xã phải làm gì, bạn phải tự động căn cứ vào chức năng, nhiệm vụ và danh sách từ khoá nhận diện dưới đây để xác định cơ quan phụ trách:

#### 2.1. Uỷ ban nhân dân xã (UBND xã)
* **Chức năng:** Cơ quan chấp hành của HĐND, cơ quan hành chính nhà nước ở địa phương. Thực hiện quản lý nhà nước trên địa bàn xã trong các lĩnh vực kinh tế - xã hội, quốc phòng, an ninh, và cung ứng dịch vụ công thiết yếu.
* **Nhiệm vụ chính:** Quản lý kinh tế, đất đai, nông nghiệp, tài nguyên, môi trường, xây dựng, giao thông, giáo dục, y tế, văn hoá, thể dục thể thao, du lịch, tư pháp, nội vụ, ngân sách, an ninh trật tự, phòng chống thiên tai, xử lý tình huống khẩn cấp, quản lý hoạt động tự quản thôn.
* **Từ khoá nhận diện:** `kinh tế, kinh tế - xã hội, phát triển kinh tế, đất đai, tài nguyên, khoáng sản, môi trường, biến đổi khí hậu, nông nghiệp, nông thôn, nông thôn mới, xây dựng nông thôn mới, thuỷ lợi, thuỷ sản, lâm nghiệp, chăn nuôi, giao thông, xây dựng, hạ tầng, cơ sở hạ tầng, quy hoạch, đô thị, văn hoá, thể dục, thể thao, du lịch, di tích, lễ hội, giáo dục, đào tạo, trường học, phổ cập giáo dục, y tế, trạm y tế, dịch bệnh, phòng chống dịch, an toàn thực phẩm, vệ sinh an toàn thực phẩm, an ninh, quốc phòng, an ninh quốc phòng, an ninh trật tự, trật tự an toàn xã hội, phòng chống tội phạm, ma tuý, phòng chống thiên tai, phòng chống lụt bão, cứu hộ cứu nạn, ứng phó sự cố, xoá đói giảm nghèo, giảm nghèo, lao động, việc làm, bảo hiểm xã hội, bảo hiểm y tế, người có công, chính sách xã hội, hộ tịch, chứng thực, tư pháp, hoà giải, thương mại, dịch vụ, công nghiệp, tiểu thủ công nghiệp, ngân sách, thuế, phí, lệ phí, tài chính, tài sản công, dịch vụ công, điện chiếu sáng, cấp nước, xử lý rác thải, phòng chống cháy nổ, hoạt động tự quản của thôn`

#### 2.2. Uỷ ban kiểm tra Đảng uỷ xã (UBKT)
* **Chức năng:** Tham mưu cho Đảng uỷ về công tác kiểm tra, giám sát và thi hành kỷ luật Đảng; trực tiếp thực hiện các nhiệm vụ chuyên môn theo quy định của Điều lệ Đảng.
* **Nhiệm vụ chính:** Kiểm tra đảng viên và tổ chức đảng khi có dấu hiệu vi phạm; giám sát chuyên đề đối với các chi bộ; tiếp nhận và giải quyết khiếu nại, tố cáo đối với đảng viên; hướng dẫn chi bộ thực hiện nghiệp vụ kiểm tra, giám sát.
* **Từ khoá nhận diện:** `kiểm tra, giám sát, kỷ luật đảng, thi hành kỷ luật, kỷ luật, vi phạm, dấu hiệu vi phạm, kiểm tra khi có dấu hiệu vi phạm, giám sát chuyên đề, khiển trách, cảnh cáo, cách chức, khai trừ, xử lý đảng viên vi phạm, suy thoái, tự diễn biến, tự chuyển hoá, kê khai tài sản, khiếu nại tố cáo đối với đảng viên, giải quyết tố cáo đảng viên, sinh hoạt đảng không đúng quy định`

#### 2.3. Ban Xây dựng Đảng
* **Chức năng:** Tham mưu, giúp việc trực tiếp cho Đảng uỷ về các mảng: Tổ chức cán bộ, Tuyên giáo và Dân vận trong Đảng bộ xã.
* **Nhiệm vụ chính:** Xây dựng phương án nhân sự, quản lý đội ngũ cán bộ; tuyên truyền chủ trương của Đảng; tổ chức học tập, quán triệt các văn bản chỉ đạo; tham mưu phát triển đảng viên mới; nâng cao chất lượng sinh hoạt chi bộ; thực hiện công tác tôn giáo, dân tộc (khía cạnh dân vận Đảng).
* **Từ khoá nhận diện:** `tổ chức cán bộ, quy hoạch cán bộ, đào tạo bồi dưỡng cán bộ, luân chuyển cán bộ, bổ nhiệm, đề bạt, sắp xếp tổ chức bộ máy, tinh giản biên chế, nhân sự, tuyên giáo, chính trị tư tưởng, giáo dục chính trị, học tập nghị quyết, quán triệt nghị quyết, sơ kết tổng kết nghị quyết, đạo đức cách mạng, học tập và làm theo, tư tưởng Hồ Chí Minh, tấm gương đạo đức, nêu gương, chuẩn mực đạo đức, xây dựng đảng, chỉnh đốn đảng, nâng cao năng lực lãnh đạo, đổi mới phương thức lãnh đạo, xây dựng tổ chức đảng, kết nạp đảng, phát triển đảng viên, chuyển đảng chính thức, đảng viên dự bị, dân vận, dân vận khéo, công tác dân vận, tôn giáo, dân tộc, tuyên truyền, đảng phí, thẻ đảng, thu hồi thẻ đảng`

#### 2.4. Uỷ ban Mặt trận Tổ quốc Việt Nam xã (MTTQ)
* **Chức năng:** Cơ quan chuyên môn về công tác Mặt trận và đoàn thể ở cấp cơ sở. Tham mưu, giúp việc Ban Thường trực MTTQ xã và các tổ chức chính trị - xã hội trực thuộc (Đoàn Thanh niên, Hội Phụ nữ, Hội Cựu chiến binh, Hội Nông dân).
* **Nhiệm vụ chính:** Vận động đoàn viên, hội viên và nhân dân; giám sát và phản biện xã hội; tổ chức phong trào thi đua; phối hợp hoạt động an sinh xã hội; hiệp thương cử ứng cử viên; tổng hợp ý kiến, kiến nghị cử tri.
* **Từ khoá nhận diện:** `mặt trận, mặt trận tổ quốc, ban thường trực mặt trận, đại đoàn kết, đoàn kết toàn dân, khối đại đoàn kết, phản biện xã hội, giám sát cộng đồng, giám sát của nhân dân, giám sát và phản biện, hiệp thương, bầu cử, ứng cử, đoàn thanh niên, hội phụ nữ, hội liên hiệp phụ nữ, hội cựu chiến binh, hội nông dân, công đoàn, các đoàn thể, tổ chức chính trị - xã hội, an sinh xã hội, từ thiện, quyên góp, ủng hộ, quỹ vì người nghèo, ngày vì người nghèo, phong trào, cuộc vận động, toàn dân, vận động nhân dân, ngày hội đại đoàn kết, ý kiến cử tri, kiến nghị cử tri, tiếp xúc cử tri`

#### 2.5. Văn phòng Đảng uỷ xã (VPĐU)
* **Chức năng:** Tham mưu, giúp việc Đảng uỷ trong tổ chức điều hành, quản lý hệ thống văn thư lưu trữ, bảo đảm hậu cần phục vụ cấp uỷ. Chủ trì công tác nội chính, phòng chống tham nhũng, lãng phí, tiêu cực của Đảng uỷ xã.
* **Nhiệm vụ chính:** Xây dựng và theo dõi quy chế làm việc của BCH Đảng bộ; tiếp nhận và quản lý văn bản đi/đến; chuẩn bị nội dung hội nghị; tổng hợp báo cáo định kỳ; ứng dụng CNTT và chuyển đổi số; công tác nội chính, phòng chống tham nhũng, lãng phí, tiêu cực; cải cách hành chính trong Đảng.
* **Từ khoá nhận diện:** `văn phòng đảng uỷ, văn thư, lưu trữ, phục vụ cấp uỷ, quy chế làm việc, chương trình công tác, tổng hợp, báo cáo định kỳ, báo cáo sơ kết, báo cáo tổng kết, hậu cần, hội nghị, phiên họp, chuyển đổi số, công nghệ thông tin, ứng dụng CNTT, nội chính, phòng chống tham nhũng, lãng phí, tiêu cực, cải cách hành chính trong đảng`

#### 2.6. Quy tắc xử lý từ khoá chồng lấn (Disambiguation Rules)

Một số cụm từ xuất hiện trong phạm vi phụ trách của nhiều cơ quan. Khi gặp tình huống này, áp dụng quy tắc ưu tiên cụm từ dài trước, sau đó phân biệt theo ngữ cảnh:

| Từ khoá chồng lấn | Ngữ cảnh → Cơ quan phụ trách |
|---|---|
| **"giám sát"** | Nếu đi kèm `"phản biện xã hội"`, `"cộng đồng"`, `"của nhân dân"` → **MTTQ**. Nếu đi kèm `"đảng viên"`, `"chi bộ"`, `"chuyên đề"`, `"dấu hiệu vi phạm"` hoặc đứng đơn lẻ trong văn bản Đảng → **UBKT**. |
| **"phòng chống tham nhũng, lãng phí, tiêu cực"** | Nếu văn bản chỉ đạo chung từ Đảng (Tỉnh uỷ, Ban Thường vụ) về công tác nội chính → **VPĐU** (chủ trì). Nếu gắn với kiểm tra, xử lý kỷ luật đảng viên tham nhũng → **UBKT**. |
| **"tuyên truyền"** | Nếu về chính trị tư tưởng, học tập nghị quyết, quán triệt chỉ đạo → **Ban Xây dựng Đảng**. Nếu về vận động quần chúng, phong trào nhân dân, cuộc vận động toàn dân → **MTTQ**. |
| **"tôn giáo, dân tộc"** | Nếu về chính sách dân vận của Đảng → **Ban Xây dựng Đảng**. Nếu về đoàn kết dân tộc, vận động nhân dân các tôn giáo → **MTTQ**. |
| **"khiếu nại, tố cáo"** | Nếu về đảng viên và tổ chức đảng → **UBKT**. Nếu về công dân, hành chính nhà nước → **UBND xã**. |

> [!NOTE]
> **Lưu ý quan trọng từ phần "Tổ chức thực hiện" của văn bản cấp trên:**
> Các văn bản chỉ đạo của Tỉnh ủy thường có phần *"Tổ chức thực hiện"*, trong đó ghi rõ chỉ đạo giao nhiệm vụ cho: *"Đảng ủy các xã, phường, thị trấn"* (hoặc *"các cấp ủy trực thuộc Tỉnh ủy"*, *"các xã"*).
> Đây là căn cứ đặc biệt quan trọng để định vị nhiệm vụ của cấp xã ở đâu (ví dụ: tuyên truyền, quán triệt, xây dựng kế hoạch triển khai, v.v.). Khi là Đảng ủy cấp xã, chúng ta cần tìm lọc chính xác những điều khoản liên quan trực tiếp đến cấp xã để chuyển hóa thành nhiệm vụ tương ứng trong công văn giao việc cấp dưới.


### 3. Quy tắc gộp nhiệm vụ đặc thù (Consolidation Rule)
Trong mẫu Công văn giao việc (`cong_van_giao_viec_mau.docx`), mặc định có 2 phần giao việc chính:
* *Nhiệm vụ 1*: Giao Ban Xây dựng Đảng tham mưu quán triệt, tuyên truyền.
* *Nhiệm vụ 2*: Giao `{{Co_quan_2}}` tham mưu triển khai thực hiện.

**Quy tắc gộp:**
* Nếu `{{Co_quan_2}}` được xác định chính là **Ban Xây dựng Đảng** (do tính chất văn bản thuần túy về công tác Đảng, cán bộ, chính trị):
  * **Hợp nhất nhiệm vụ:** Gộp nhiệm vụ 1 và nhiệm vụ 2 thành một đoạn văn duy nhất:
    > *"1. Giao Ban Xây dựng Đảng tham mưu Ban Thường vụ Đảng uỷ quán triệt, tuyên truyền và triển khai thực hiện [Tên văn bản cấp trên]; trình Thường trực Đảng uỷ trước [Ngày đến hạn 1]."*
  * **Xóa bỏ đoạn văn thứ 2:** Xóa hoàn toàn đoạn văn chứa biến nhiệm vụ thứ hai (`2. Giao {{Co_quan_2}}...`) ra khỏi tài liệu Word để tránh lặp lại thông tin dư thừa.
  * **Lưu ý:** Nếu chỉ có 1 công việc được giao thì không đánh số thứ tự. Không hiển thị "1." trước đoạn văn bản.

### 4. Quy tắc Kính gửi tối giản (Recipient Filtering Rule)
* **Nguyên tắc:** *"Chỉ gửi cho đơn vị được giao nhiệm vụ"*.
* Biến `{{DANH_SACH_GUI}}` (hoặc `{{DANH_SACH_KINH_GUI}}`) chỉ chứa danh sách các đơn vị thực sự có nhiệm vụ được giao trong phần thân công văn.
* **Thứ tự Kính gửi:** Sắp xếp danh sách Kính gửi theo thứ tự ưu tiên hành chính như sau:
  1. **Ủy ban nhân dân xã**
  2. **Ủy ban Mặt trận Tổ quốc Việt Nam xã**
  3. **Ban Xây dựng Đảng**
  4. **Ủy ban kiểm tra Đảng ủy xã**
  5. **Văn phòng Đảng uỷ xã**
* **Ví dụ:** Nếu công văn gộp cả 2 nhiệm vụ cho Ban Xây dựng Đảng $\rightarrow$ Danh sách kính gửi chỉ hiển thị duy nhất `Ban Xây dựng Đảng.` 

### 5. Quy tắc ngày đến hạn mặc định (Default Deadline Rule)
* **Nguyên tắc:** Đối với các văn bản cấp trên có thể loại là **Kế hoạch**, **Nghị quyết**, hoặc **Chương trình hành động** mà trong nội dung văn bản không chỉ rõ thời hạn cụ thể giao cho Đảng ủy xã:
  * **Thời gian mặc định:** Gán ngày đến hạn là **10 ngày** kể từ ngày xây dựng công văn.
  * **Tránh ngày nghỉ:** Nếu ngày đến hạn rơi vào ngày thứ Bảy hoặc Chủ nhật, tự động cộng thêm số ngày để lùi sang **thứ Hai liền kề**.

### 6. Quy chuẩn đặt dấu tiếng Việt (Tone Mark Style Rule)
* **Nguyên tắc:** Sử dụng kiểu đặt dấu thanh truyền thống (cũ) thay vì kiểu mới để bảo đảm đúng thể thức văn bản hành chính Đảng:
  * Đặt dấu thanh trên các nguyên âm dài và hợp âm: **`oà`**, **`uý`**, **`uỷ`**, etc. (thay vì `òa`, `úy`, `ủy`, etc.).
  * Ví dụ: viết **`Đảng uỷ`**, **`Thường trực Đảng uỷ`**, **`Uỷ ban nhân dân`**, **`hoà`**, v.v.

---

## 🎨 Quy chuẩn định dạng Văn bản (Formatting Standards)

Áp dụng nghiêm ngặt các quy định về Font chữ và cách trình bày theo Hướng dẫn số 05-HD/VPTW:

1. **Trích yếu công văn (`{{TRICH_YEU_CONG_VAN}}`)**:
   * Font chữ: **Times New Roman**
   * Kích thước: **12pt**
   * Kiểu dáng: **Chữ nghiêng (Italic)**
   * Căn lề: **Căn giữa (Center)**
2. **Kính gửi (`{{DANH_SACH_KINH_GUI}}` / `{{DANH_SACH_GUI}}`)**:
   * Font chữ: **Times New Roman**
   * Kích thước: **14pt**
   * Căn lề: **Căn lề trái (Left)**
   * Mỗi đơn vị bắt đầu bằng dấu `- `, ngăn cách bằng dấu `;`, đơn vị cuối cùng kết thúc bằng dấu `.`.
   * Nếu chỉ có 1 đơn vị được giao việc thì không đánh dấu "-" trước tên đơn vị.
3. **Nội dung giao việc (Toàn bộ các đoạn văn thân bài chỉ đạo)**:
   * Font chữ: **Times New Roman**
   * Kích thước: **14pt**
   * Thụt đầu dòng: **1 cm** cho dòng đầu tiên của mỗi đoạn văn bản.
   * **Quy định nổi bật:** Cụm từ thông báo thời hạn hoàn thành có dạng **`trước ngày DD/MM/YYYY`** hoặc **`trước DD/MM/YYYY`** bắt buộc phải được **bôi đậm và in nghiêng** (Ví dụ: ***trước ngày 10/07/2026***).
4. **Nơi nhận (Distribution List)**:   
   * Giữ nguyên cấu trúc mặc định của mẫu (template):
     ```text
     Nơi nhận:
     - Như trên;
     - Lưu VPĐU.
     ```

---

## 🛠️ Cấu trúc thư mục & Cách vận hành

### 1. Cấu trúc thư mục chuẩn
```text
taovanban_khoidang/
│
├── SKILL.md                 # Tệp định nghĩa này (Bộ não của kỹ năng)
├── references/
│   └── cong_van_giao_viec_mau.docx  # Tệp mẫu Word gốc chứa các thẻ biến
├── scripts/
│   ├── generate_docx.py     # Script Python thực thi điền mẫu, định dạng và gộp paragraph
│   ├── run_generation.py   # Script tự động hóa chuẩn bị dữ liệu và gọi generate_docx.py
│   └── input_84.json        # Dữ liệu JSON đầu vào mẫu cho Kế hoạch 84-KH/TU
└── output/
    └── CV tham mưu KH TU về chuẩn mực đạo đức cách mạng.docx  # File Word đầu ra đặt tên theo chuẩn quy ước

```

### 2. Dữ liệu JSON đầu vào chuẩn
```json
{
  "van_ban_cap_tren": "Kế hoạch số 84-KH/TU, ngày 15/6/2026 của Tỉnh ủy về triển khai thực hiện Quy định chuẩn mực đạo đức cách mạng của cán bộ, đảng viên, công chức, viên chức thuộc Đảng bộ và hệ thống chính trị tỉnh Khánh Hòa trong giai đoạn mới",
  "Ngay_den_han_1": "15/07/2026",
  "Co_quan_2": "Ban xây dựng Đảng",
  "ngay_den_han_2": "15/07/2026",
  "TRICH_YEU_CONG_VAN": "V/v triển khai thực hiện Kế hoạch số 84-KH/TU ngày 15/6/2026 của Tỉnh ủy",
  "DANH_SACH_NOI_NHAN": [
    "Thường trực Đảng ủy",
    "Các chi bộ trực thuộc",
    "Lưu VPĐU"
  ]
}
```

### 3. Lệnh chạy sinh văn bản
Để chạy sinh văn bản tự động từ dòng lệnh:
```powershell
python scripts/generate_docx.py <đường_dẫn_file_json_đầu_vào> <đường_dẫn_file_docx_đầu_ra>
```
*Tập lệnh `generate_docx.py` sẽ tự động thực hiện nạp dữ liệu, kiểm tra quy tắc gộp của `Co_quan_2`, xóa các đoạn thừa, tự động tính toán danh sách đơn vị kính gửi thực tế, và định dạng lề thụt đầu dòng 1cm cũng như font Times New Roman 12/14pt tương ứng.*

### 4. Quy tắc đặt tên file đầu ra (Output Naming Convention)
Tên tệp tin Word (.docx) được tạo ra phải tuân theo đúng định dạng:
`CV tham mưu [thể loại văn bản cấp trên viết tắt, ví dụ KH, NQ, CV, ....] TU về [ngắn gọn nhất có thể, chỉ để đọc qua và hình dung ra, ví dụ: về chuẩn mực đạo đức cách mạng].docx`

*Ví dụ minh họa:*
* Kế hoạch (KH) số 84-KH/TU về đạo đức cách mạng $\rightarrow$ `CV tham mưu KH TU về chuẩn mực đạo đức cách mạng.docx`
* Nghị quyết (NQ) số 15-NQ/TU về chuyển đổi số $\rightarrow$ `CV tham mưu NQ TU về chuyển đổi số.docx`
* Chỉ thị (CT) số 05-CT/TW về học tập tấm gương đạo đức $\rightarrow$ `CV tham mưu CT TU về học tập tấm gương đạo đức.docx`

### 5. Quy tắc dọn dẹp các tệp tạm thời (Clean-up Rule)
* **Nguyên tắc:** Giữ cho thư mục làm việc và các thư mục mã nguồn (`scripts/`) luôn sạch sẽ và chỉ chứa các tệp tin cốt lõi được định nghĩa trong cấu trúc thư mục chuẩn.
* **Hành động:**
  * Không tạo ra các file runner trung gian hoặc dữ liệu JSON trung gian cho từng văn bản trong thư mục `scripts/` (ví dụ: tránh lưu các file dạng `run_generation_82.py` hay `input_82.json` tại đây).
  * Mọi tệp tin chạy thử nghiệm, log trung gian hoặc bản nháp OCR phát sinh trong quá trình phát triển phải được xóa hoặc đưa vào thư mục tạm/scratch của hệ thống sau khi đã hoàn thành tác vụ.
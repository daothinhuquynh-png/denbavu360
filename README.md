# Đền Bà Vũ 360° — Tour thực tế ảo

Phần mềm tham quan thực tế ảo (virtual tour) cho **Đền Bà Vũ** — Di tích lịch sử
cấp Quốc gia (1993), thờ Thánh Mẫu Vũ Nương (Vũ Thị Thiết, nhân vật *Chuyện người
con gái Nam Xương*), xã Bắc Lý, huyện Lý Nhân, tỉnh Hà Nam.

Người dùng đứng giữa từng điểm trong đền, kéo nhìn 360°, bấm mũi tên để "đi" sang
điểm khác, bấm điểm chú thích để đọc thông tin. Tour gồm **18 điểm chụp**.

> Đây cũng là **khuôn mẫu tái sử dụng** cho các di tích khác (thuộc bộ sản phẩm
> *HeritaVault*). Muốn làm tour mới: thay thư mục `panos/` + viết lại `tour.json`.

---

## 1. Công nghệ

| Thành phần | Lựa chọn | Ghi chú |
|---|---|---|
| Thư viện 360° | **Pannellum 2.5.6** (MIT) | Vendor sẵn trong `vendor/`, **chạy offline** |
| Định dạng ảnh | JPG **equirectangular** 2:1 | Gốc 11968×5984, bản web hạ còn 6000px |
| Cấu hình tour | `tour.json` (thuần dữ liệu) | Tách hẳn khỏi code |
| Server | Tĩnh bất kỳ | `serve.py` chỉ cần khi **chỉnh** tour |

Không dùng framework, không build step, không phụ thuộc internet. Mở bằng trình
duyệt là chạy.

## 2. Cấu trúc thư mục

```
tour/
├── index.html        # BẢN XEM tour (deploy cái này) — chỉ đọc tour.json
├── builder.html      # TRÌNH DỰNG tour (công cụ soạn, dùng nội bộ với serve.py)
├── tour.json         # DỮ LIỆU tour: tên di tích, điểm, ảnh, mũi tên, chú thích
├── serve.py          # Server tĩnh + GET /panos + ghi tour.json (POST /save)
├── panos/            # Ảnh 360° bản web (01.jpg … 18.jpg)
├── vendor/           # Pannellum (pannellum.js, pannellum.css) — bản offline
└── README.md         # Tài liệu này

../pic/               # ẢNH GỐC độ phân giải đầy đủ (lưu trữ, KHÔNG đẩy lên web)
../DenBaVu360/        # File gốc máy Insta360 (.insp/.dng) + Sơ đồ.xlsx (kịch bản)
```

## 3. Chạy thử

```bash
cd tour
python3 serve.py            # mở http://localhost:8099/
```
Hoặc với bất kỳ server tĩnh nào (khi chỉ XEM, không chỉnh):
```bash
python3 -m http.server 8099
```
> ⚠️ Không mở trực tiếp `file://index.html` — trình duyệt chặn `fetch("tour.json")`.
> Phải qua HTTP server.

## 4. Mô hình dữ liệu (`tour.json`)

```jsonc
{
  "first": "p1",                       // cảnh mở đầu
  "order": ["p1", ..., "p18"],         // thứ tự hiển thị ở bảng trái
  "names": { "p1": "Cổng Đền Bà Vũ", ... },   // tên hiển thị của từng điểm
  "scenes": {
    "p4": {
      "panorama": "panos/04.jpg",
      "hotSpots": [
        // Mũi tên đi sang cảnh khác:
        { "id": "l1", "type": "scene", "sceneId": "p7", "yaw": 0,   "pitch": -3 },
        // Điểm chú thích:
        { "id": "i1", "type": "info",  "text": "…",      "yaw": -90, "pitch": 0 }
      ]
    }
  }
}
```

- `id`: định danh hotspot **trong một cảnh** (dùng để thêm/xoá động khi chỉnh).
- `yaw`: góc ngang, **0° = giữa ảnh**, +phải / −trái, ±180° = phía sau.
- `pitch`: góc dọc, 0 = ngang tầm mắt, âm = nhìn xuống.
- `type:"scene"` → bấm vào nhảy sang `sceneId`. `text` tự lấy từ `names`.
- `type:"info"` → bấm/rê hiện `text`.

**Sơ đồ nối điểm gốc** nằm ở `../DenBaVu360/Sơ đồ.xlsx` (mô tả trái/phải/thẳng/sau
cho từng điểm + sơ đồ mặt bằng) — nguồn để dựng `tour.json`.

## 5. Trình dựng tour — `builder.html` (không cần biết code)

Mở `http://localhost:8099/builder.html` (phải chạy qua `serve.py`). Toàn bộ thao
tác bằng chuột, **tự lưu** vào `tour.json` sau mỗi thay đổi.

- **Thêm điểm**: bỏ ảnh 360° đã nén vào `panos/` → bấm *➕ Thêm điểm từ ảnh* →
  chọn file, đặt tên. (Trình dựng đọc danh sách ảnh qua `GET /panos`.)
- **Nối lối đi**: chọn điểm đích ở ô trên cùng cột phải → *➕ Thêm lối đi* → bấm
  lên ảnh nơi đặt mũi tên.
- **Chú thích**: *➕ Thêm điểm chú thích* → gõ nội dung → bấm lên ảnh.
- **Di chuyển / sửa / xoá**: mỗi mũi tên có nút ✥ (di chuyển) ✎ (sửa chữ) 🗑 (xoá).
- **Điểm**: ★ đặt điểm mở đầu · ↑↓ đổi thứ tự · ✎ đổi tên · 🗑 xoá.
- **Tên di tích**: nút *✎ Tên di tích* trên thanh trên → đặt `title`/`subtitle`
  (bản xem `index.html` tự hiển thị, nên dùng được cho mọi đền).

Cơ chế đặt vị trí: lấy toạ độ bằng `viewer.mouseEventToCoords()` (cú bấm gọn,
không kéo). Pannellum 2.5.6 **không** hỗ trợ kéo–thả hotspot nên dùng "bấm để đặt".

### Tạo tour cho một đền MỚI
1. Chép cả thư mục `tour/` sang thư mục đền mới, xoá `panos/*` và `tour.json`.
2. Bỏ ảnh 360° đã nén (xem mục 6) vào `panos/`.
3. `python3 serve.py` → mở `builder.html` → đặt tên di tích, thêm điểm, nối lối đi,
   gõ chú thích. Builder tự tạo `tour.json` từ đầu.
4. Deploy `index.html` + `tour.json` + `panos/` + `vendor/` (mục 7).

## 6. Quy trình tạo ảnh (từ máy Insta360)

1. Chụp bằng Insta360, xuất qua **Insta360 Studio** → JPG **equirectangular**
   11968×5984, bật FlowState/cân chỉnh chân trời.
2. Nén bản web (giữ nguyên gốc trong `../pic/`):
   ```bash
   sips -Z 6000 -s format jpeg -s formatOptions 62 pic/N.jpg --out tour/panos/0N.jpg
   ```
   (~40MB → ~3MB, vẫn 6000px.)

## 7. Triển khai (deploy)

Tour là **web tĩnh** → host miễn phí:
- **GitHub Pages / Netlify**: đẩy thư mục `tour/` lên là xong (không cần `serve.py`).
- **Offline USB**: copy cả thư mục `tour/`, mở bằng một server tĩnh nhỏ trên máy
  trưng bày (vì cần HTTP để đọc `tour.json`).

Sau khi chốt nội dung, bọc thêm một trang giới thiệu rồi tạo **mã QR** trỏ tới URL.

## 8. Giấy phép / ghi công

- Pannellum © Matthew Petroff — giấy phép **MIT** (xem `vendor/`).
- Ảnh 360° và nội dung di tích: thuộc dự án số hoá Đền Bà Vũ.

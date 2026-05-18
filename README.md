#Phát hiện bệnh trên lá lúa bằng phương pháp học sâu
Ngành nông nghiệp đóng vai trò quan trọng trong sự phát triển kinh tế của bất kỳ quốc gia nào. Về nguyên liệu thô, đa số các quốc gia đều phụ thuộc vào hàng hóa nông nghiệp. Lúa là cây trồng được canh tác nhiều nhất trên toàn cầu. Lúa được trồng ở hơn 100 quốc gia trên thế giới. Tổng cộng 158 triệu ha được thu hoạch mỗi năm, cho năng suất hơn 700 triệu tấn gạo. So với các châu lục khác, châu Á sản xuất phần lớn lúa. Do dân số ngày càng tăng, ngành này đang ảnh hưởng đến môi trường về mặt nóng lên toàn cầu, biến đổi khí hậu nhanh chóng (Yadav et al., 2021). Ảnh lá lúa được chụp bằng máy ảnh kỹ thuật số hoặc thiết bị tương tự, và các hình ảnh này được sử dụng để phân loại vùng bị ảnh hưởng trên lá. Để phát hiện bệnh trên lá lúa, chúng tôi sử dụng mạng nơ-ron tích chập và mạng nơ-ron sâu trong khung đề xuất. Bài báo này đề xuất một khung sử dụng phần mềm mã nguồn mở, chi phí thấp để thực hiện nhiệm vụ phát hiện bệnh thực vật một cách đáng tin cậy.

#Bài toán
Phát hiện bệnh trên lá lúa bằng kỹ thuật xử lý ảnh và học sâu. ##Đặc điểm của dự án

Sử dụng các thuật toán học sâu.
Mô hình được sử dụng là mô hình CNN.
Thuật toán được sử dụng là thuật toán học có giám sát dựa trên lan truyền ngược để huấn luyện.
Sử dụng Flask để tạo giao diện lập trình ứng dụng, tức là API, cùng với hệ thống mẫu Jinja2.
Các trang web tĩnh được tạo ra để hiển thị kết quả/dự đoán về bệnh lá lúa bằng cách sử dụng các công nghệ giao diện người dùng như HTML, CSS và Bootstrap.
Độ chính xác của mô hình là 90%.
Tỷ lệ dữ liệu huấn luyện và kiểm thử là 8:2, điều này có thể dẫn đến hiện tượng quá khớp (overfitting) của mô hình.
Tuy nhiên, trong quá trình thử nghiệm bộ dữ liệu, chúng tôi đã cung cấp bộ dữ liệu của riêng mình.
#Đóng góp
Tạo bộ dữ liệu riêng. Đối với dự án này, tôi đã sử dụng các bộ dữ liệu từ Kaggle cũng như bộ dữ liệu riêng của mình. Tạo các trang web.

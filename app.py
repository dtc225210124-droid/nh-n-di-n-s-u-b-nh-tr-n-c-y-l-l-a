from flask import Flask, request, render_template
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
import cv2

app = Flask(__name__)

# Load model 1 lần
model = load_model('cnn_dwnld_model.h5', compile=False)

# Thông tin bệnh
disease_info = {

    "bacterial_leaf_blight": {
        "name": "Bacterial Leaf Blight (Bệnh bạc lá)",

        "symptoms": """
        Mép lá chuyển vàng rồi khô trắng.
        Vết bệnh lan dọc theo phiến lá.
        Lá bị cháy khô từ chóp xuống.
        """,

        "cause": """
        Do vi khuẩn Xanthomonas oryzae pv. oryzae gây ra.
        """,

        "prevention": """
        Sử dụng giống kháng bệnh, vệ sinh đồng ruộng
        và không bón quá nhiều đạm.
        """,

        "treatment": """
        Sử dụng thuốc chứa Copper Hydroxide
        hoặc Streptomycin theo hướng dẫn.
        """
    },

    "bacterial_leaf_streak": {
        "name": "Bacterial Leaf Streak (Bệnh đốm sọc vi khuẩn)",

        "symptoms": """
        Lá xuất hiện các sọc nhỏ màu vàng nâu.
        Các vết bệnh kéo dài theo gân lá.
        """,

        "cause": """
        Do vi khuẩn Xanthomonas oryzae pv. oryzicola gây ra.
        """,

        "prevention": """
        Giữ ruộng thông thoáng, tránh tưới nước quá nhiều
        và dùng giống sạch bệnh.
        """,

        "treatment": """
        Loại bỏ lá bệnh và sử dụng thuốc gốc đồng khi cần thiết.
        """
    },

    "bacterial_panicle_blight": {
        "name": "Bacterial Panicle Blight (Bệnh lép vàng/trắng)",

        "symptoms": """
        Hạt lúa bị lép, chuyển màu vàng hoặc trắng.
        Bông lúa khô và phát triển kém.
        """,

        "cause": """
        Do vi khuẩn Burkholderia glumae gây ra.
        """,

        "prevention": """
        Gieo trồng đúng thời vụ và tránh mật độ quá dày.
        """,

        "treatment": """
        Phun thuốc kháng khuẩn phù hợp theo khuyến cáo nông nghiệp.
        """
    },

    "blast": {
        "name": "Leaf Blast (Bệnh đạo ôn)",

        "symptoms": """
        Xuất hiện các đốm hình thoi màu xám ở giữa
        và viền nâu ở mép.
        Lá có thể cháy khô nặng.
        """,

        "cause": """
        Do nấm Pyricularia oryzae gây ra.
        """,

        "prevention": """
        Không bón quá nhiều đạm, gieo cấy mật độ hợp lý
        và sử dụng giống kháng bệnh.
        """,

        "treatment": """
        Phun thuốc chứa Tricyclazole hoặc Isoprothiolane.
        """
    },

    "brown_spot": {
        "name": "Brown Spot (Bệnh đốm nâu)",

        "symptoms": """
        Lá xuất hiện các đốm nâu tròn hoặc bầu dục.
        Trung tâm đốm có màu xám nhạt.
        """,

        "cause": """
        Do nấm Bipolaris oryzae gây ra.
        """,

        "prevention": """
        Bón phân cân đối, đặc biệt bổ sung kali
        và giữ ruộng thông thoáng.
        """,

        "treatment": """
        Phun thuốc Mancozeb hoặc Carbendazim.
        """
    },

    "dead_heart": {
        "name": "Dead Heart (Chồi non bị héo)",

        "symptoms": """
        Chồi non bị vàng úa và khô chết.
        Cây lúa còi cọc, không phát triển.
        """,

        "cause": """
        Chủ yếu do sâu đục thân gây hại.
        """,

        "prevention": """
        Kiểm tra đồng ruộng thường xuyên
        và diệt sâu đục thân sớm.
        """,

        "treatment": """
        Sử dụng thuốc trừ sâu phù hợp theo hướng dẫn địa phương.
        """
    },

    "downy_mildew": {
        "name": "Downy Mildew (Bệnh sương mai)",

        "symptoms": """
        Lá có lớp mốc trắng hoặc xám nhạt.
        Lá úa vàng và phát triển kém.
        """,

        "cause": """
        Do nấm giả thuộc nhóm Oomycetes gây ra.
        """,

        "prevention": """
        Giảm độ ẩm trên ruộng và tránh trồng quá dày.
        """,

        "treatment": """
        Phun thuốc Metalaxyl hoặc Mancozeb.
        """
    },

    "hispa": {
        "name": "Hispa (Sâu gai, bọ gai)",

        "symptoms": """
        Lá bị cào trắng thành từng đường dài.
        Lá khô và giảm khả năng quang hợp.
        """,

        "cause": """
        Do côn trùng Hispa gây hại trên lá lúa.
        """,

        "prevention": """
        Vệ sinh đồng ruộng và loại bỏ lá bị hại.
        """,

        "treatment": """
        Sử dụng thuốc trừ sâu sinh học
        hoặc thuốc đặc trị Hispa.
        """
    },

    "normal": {
        "name": "Healthy (Cây khỏe mạnh)",

        "symptoms": """
        Lá xanh đều, không có đốm bệnh,
        cây phát triển bình thường.
        """,

        "cause": """
        Cây không bị nhiễm bệnh.
        """,

        "prevention": """
        Tiếp tục chăm sóc đúng kỹ thuật
        và kiểm tra sâu bệnh định kỳ.
        """,

        "treatment": """
        Cây khỏe mạnh, chưa cần điều trị.
        """
    },

    "tungro": {
        "name": "Tungro (Bệnh vàng lùn)",

        "symptoms": """
        Cây lúa bị lùn, lá vàng cam,
        giảm số lượng chồi và hạt lép nhiều.
        """,

        "cause": """
        Do sự kết hợp giữa RTBV và RTSV virus gây ra.
        """,

        "prevention": """
        Diệt rầy xanh truyền bệnh
        và sử dụng giống kháng Tungro.
        """,

        "treatment": """
        Loại bỏ cây nhiễm nặng
        và kiểm soát côn trùng truyền bệnh.
        """
    }
}
# Chuyển ảnh thành tensor
def convert_img_to_tensor2(fpath):

    img = cv2.imread(fpath)

    # Kiểm tra ảnh có đọc được không
    if img is None:
        return None

    img = cv2.resize(img, (256, 256))

    res = img_to_array(img)

    res = np.array(res, dtype=np.float32) / 255.0

    res = res.reshape(1, 256, 256, 3)

    return res


# Dự đoán
def check(res):

    classes = [
        "bacterial_leaf_blight",
        "bacterial_leaf_streak",
        "bacterial_panicle_blight",
        "blast",
        "brown_spot",
        "dead_heart",
        "downy_mildew",
        "hispa",
        "normal",
        "tungro"
    ]

    pred = model.predict(res)

    result = np.argmax(pred)

    disease = classes[result]

    confidence = float(np.max(pred)) * 100

    info = disease_info[disease]

    return {

        "name": info["name"],

        "symptoms": info["symptoms"],

        "cause": info["cause"],

        "prevention": info["prevention"],

        "treatment": info["treatment"],

        "confidence": round(confidence, 2)
    }


@app.route('/testown', methods=['POST', 'GET'])
def test():

    if request.method == 'POST':

        img = request.files['img']

        # Lưu ảnh
        img.save('static/h.jpg')

        # Chuyển ảnh
        res = convert_img_to_tensor2("static/h.jpg")

        # Nếu lỗi đọc ảnh
        if res is None:

            return render_template(
                'result.html',
                disease="Không thể đọc ảnh",
                symptoms="Ảnh không hợp lệ.",
                cause="Không xác định",
                prevention="Hãy thử ảnh khác.",
                treatment="Không có",
                confidence=0
            )

        # Dự đoán
        msg = check(res)

        return render_template(

            'result.html',

            disease=msg["name"],

            symptoms=msg["symptoms"],

            cause=msg["cause"],

            prevention=msg["prevention"],

            treatment=msg["treatment"],

            confidence=msg["confidence"]

        )

    return render_template('rice.html')


@app.route('/a', methods=['POST', 'GET'])
def choose():

    if request.method == 'POST':

        name = request.form.get("datasets")

        if name == "created":
            return render_template('riceown.html')

        else:
            return render_template('rice.html')

    return render_template('choosedataset.html')


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":

            return render_template('choosedataset.html')

        else:

            return render_template(
                'login.html',
                msg="Login failed"
            )

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
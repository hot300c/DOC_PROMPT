// https://app.eraser.io/workspace/jJyuLRyhNPoe5TSZXr80
// eraser

direction right
// cloud-architecture-diagram

Client [icon: users] {
    Web Browser [icon: monitor] {
        Web app [icon: browser]
    }
    Mobile Apps [icon: mobile] {
        iOS App [icon: apple]
        Android App [icon: android]
    }
    Zalo [icon: message]
    Web Admin [icon: browser]
}

group PNT Infrastructure {
  APIGW Gateway [icon: aws-api-gateway]
    
    
    //prompt: nhóm lại thành 1 group
    BACKEND {
        rentcar-backend-service [icon: k8s-pod, note: "ip:112, port:7090", color: blue]
        database-rentcar [icon: database, color: red] {
          db-rentcar [icon: database]
          db-website-rentcar [icon: database]
        }
    }

        Keycloak [icon: key] // chứng thực người dùng
    Firebase [icon: firebase] // gửi notification
    S3 Storage [icon: aws-s3] // lưu hình ảnh người dùng
}

group FLY.io Infrastructure {
  node-zca-service [icon: nodejs]
}

group external Infrastructure {
  Firebase [icon: firebase, note: "external"]
  OpenAI API [icon: cloud, note: "external"]
}




// prompt: thêm gateway kết nối đến
Client > APIGW Gateway
Web Admin -> APIGW Gateway: quản trị hệ thống
rentcar-backend-service -> db-rentcar
APIGW Gateway > rentcar-backend-service


// thêm kết nối mới
rentcar-backend-service -> Keycloak: xác thực người dùng
rentcar-backend-service -> Firebase: push notification
Mobile Apps -> rentcar-backend-service: REST API
Mobile Apps -> S3 Storage: tải ảnh người dùng

Web app -> db-website-rentcar: truy vấn dữ liệu website

Zalo -> node-zca-service: gửi thông tin
node-zca-service -> OpenAI API: gọi API

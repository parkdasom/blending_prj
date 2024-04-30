// your_script.js

// 알림을 모달에 표시하는 함수
function showNotificationModal(content) {
    // 알림 내용 설정
    document.getElementById('notificationContent').innerText = content;
    // 모달 표시
    $('#notificationModal').modal('show');
}

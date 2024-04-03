// SocketIO 연결
var socket = io();

// 공지사항 업데이트 이벤트 핸들러
socket.on('new_announcement', function(data) {
    // 공지사항 업데이트 처리
    console.log('New announcement:', data.title, data.content);
});

// 신청 상태 변경 이벤트 핸들러
socket.on('status_changed', function(data) {
    // 신청 상태 변경 처리
    console.log('Application status changed:', data.id, data.status);
});

// 연결 해제 이벤트 핸들러
socket.on('disconnect', function() {
    console.log('Disconnected from server');
});
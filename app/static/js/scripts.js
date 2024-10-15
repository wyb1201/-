// 导航栏-使用说明
document.addEventListener('DOMContentLoaded', function () {
    var popoverElements = document.querySelectorAll('[data-bs-toggle="popover"]');

    popoverElements.forEach(function (element) {
        new bootstrap.Popover(element, {
            trigger: 'hover focus' // 启用悬停和焦点触发
        });
    });
});

// ai问答
$(function () {
    $('#sendBtn').on('click', function () {
        const userInput = $('#userInput').val();
        if (userInput) {
            // 将用户输入添加到聊天框
            $('#chatbox').append(`<div class="user-message"><strong>你:</strong> <span>${userInput}</span></div>`);
            $('#userInput').val(''); // 清空输入框
            $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight); // 滚动到底部


            // 发送请求到后端
            $.ajax({
                url: '/ask', // 后端处理问题的路由
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({question: userInput}),
                success: function (response) {
                    $('#chatbox').append(`<div class="ai-message"><strong>小智:</strong><br>
                                                <strong>知识点:</strong>${response.acknowledge}<br>
                                                <strong>相关网址:</strong><a href="${response.b_url}" target="_blank">${response.b_url}</a><br>
                                                <strong>回答:</strong>${response.reply}</div>`);
                    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight); // 滚动到底部
                },
                error: function () {
                    $('#chatbox').append(`<div class="ai-message"><strong>小智:</strong> 出现错误，请重试</div>`);
                }
            });
        } else {
            alert('请先输入问题');
        }
    });
});

// 上传-生成
$(function () {
    let imagePath; // 脑图路径

    // 点击上传时
    $('#filePass').on('click', function () {
        // 接收文件
        var fileInput = document.getElementById('input');
        var file = fileInput.files[0];

        if (file) {
            var formData = new FormData();
            formData.append('file', file);

            // 等待画面
            $('#loadingModal').modal('show');

            //视频传给后端
            $.ajax({
                url: '/upload',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {

                    // 生成视频、大纲
                    var video_path = data.video_path;
                    var video_prompt = data.video_prompt.contents;

                    // 视频路径
                    video_path = video_path.split('\\').slice(1).join('/');
                    console.log("Video path received:", video_path); // 打印视频路径

                    // 尝试加载大纲内容
                    let newRows = [];
                    try {
                        newRows = video_prompt.map(item => {
                            var [time, reduce] = item.end_time.split(',');
                            return `<tr>
                                                <td style="font-size: 13px; color: #61666D;">${time}</td>
                                                <td style="font-size: 13px;">${item.topic}</td>
                                                </tr>`;
                        });
                    } catch (error) {
                        console.error('大纲加载失败:', error);
                        alert('大纲加载失败，请稍后再试');
                    }

                    // 加载大纲整体
                    if (newRows.length > 0) {
                        $('#dg tbody').append(newRows.join(''));
                        //  大纲生成后自动展开
                        $('#panelsStayOpen-collapseOne').collapse('show');
                    }

                    // 手动调整chatbox的高度
                    $('#chatbox').css('height', 'auto'); // 重置高度
                    $('#chatbox').height($('#chatbox')[0].scrollHeight); // 根据内容调整高度


                    // 尝试加载时间轴节点
                    let prompt = [];
                    try {
                        prompt = video_prompt.map(item => {
                            return {
                                words: item.topic,
                                time: parseTime(item.end_time)
                            };
                        });
                        // 成功初始化视频
                        var videoObject = {
                            container: '.video',
                            prompt: prompt,
                            video: video_path
                            // '../static/uploads/IMG_7281.mp4'
                        };
                        new ckplayer(videoObject);
                    } catch (error) {
                        console.error('时间轴节点加载失败:', error);
                        alert('时间轴节点加载失败，请稍后再试');
                        // 初始化视频
                        var videoObject = {
                            container: '.video',
                            video: video_path
                            // '../static/uploads/IMG_7281.mp4'
                        };
                        new ckplayer(videoObject);
                    }

                    // 脑图
                    try{
                        imagePath = data.image_path.split('\\').slice(1).join('/');
                        $('#generateMindmap').prop('disabled', false); // 启用脑图按钮
                    }catch(error){
                        console.error('脑图加载失败:', error);
                        alert('脑图加载失败，请稍后再试');
                    }


                    // 隐藏等待画面
                    $('#loadingModal').modal('hide');
                    $('.modal-backdrop').remove();
                    $('body').css('overflow', 'auto');
                },
                error: function () {
                    alert('文件上传失败，请重新输入密钥，上传视频');
                    // 隐藏等待画面
                    $('#loadingModal').modal('hide');
                    $('.modal-backdrop').remove();
                }
            });
        } else {
            alert('请选择一个文件');
        }
    });

    // 点击生成脑图按钮
    $('#generateMindmap').on('click', function () {
        $('#generatedImage').attr('src', imagePath) // 加载脑图
        $('#image-modal').modal('show');
    });


    // 00:00:01,120 时间转为秒/s
    function parseTime(endTime) {
        const [hours, minutes, seconds] = endTime.split(':');
        return parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseFloat(seconds.replace(',', '.'));
    }
});


// sideBar切换open类 展开/回收
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

//保存api密钥
$(function () {
    $('#button-addon2').on('click', function () {
        const input = $('#key').val();
        if (input) {
            $('#key').val('');

            //给后端
            $.ajax({
                url: '/key',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({apiKey: input}),
                success: function () {
                    console.log('密钥已成功保存');
                    $('#successToast').toast({delay: 3000});
                    $('#successToast').fadeIn().toast('show');
                },
                error: function () {
                    console.error('保存密钥失败');
                }
            })
        }
    })
})



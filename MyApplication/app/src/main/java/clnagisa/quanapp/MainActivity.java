package clnagisa.quanapp;


import android.app.Activity;
import android.app.AlertDialog;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Base64;
import android.view.KeyEvent;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;


public class MainActivity extends Activity {

    private static final int NOTIFICATION_ID_1 = 1;
    private static final int MY_DIALOG_ID = 1 ;
    private WebView webView;
    private Bitmap bitmap = null;
    private Context mContext = null;
    private String url = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = this;
        final EditText text = (EditText)findViewById(R.id.editText);
        Button button = (Button)findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                url = text.getText().toString();
                init(url);
            }
        });

        new Thread(socketRun).start();

        Button stop = (Button)findViewById(R.id.stop);
        stop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new Thread(send).start();
            }
        });

    }


    @Override     //重写返回键的函数
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            //写下你希望按下返回键达到的效果代码，不写则不会有反应
            moveTaskToBack(true);//返回键不会销毁当前的activity，而已隐藏在后台继续运行，相当于home键
            return false;
        }
        return super.onKeyDown(keyCode, event);
    }

    //弹出通知栏函数
    public void tongzhilan() {
        NotificationManager myManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        PendingIntent pi = PendingIntent.getActivity(
                mContext,
                100,
                new Intent(mContext, MainActivity.class),
                PendingIntent.FLAG_CANCEL_CURRENT
        );   //定义一个PendingIntent，点击Notification后启动一个Activity
        //2.通过Notification.Builder来创建通知
        Notification.Builder myBuilder = new Notification.Builder(mContext);
        myBuilder.setContentTitle("有陌生人进入（点击查看）")
                //设置状态栏中的小图片，尺寸一般建议在24×24，这个图片同样也是在下拉状态栏中所显示
                .setSmallIcon(R.mipmap.ic_launcher)
                //设置默认声音和震动
                .setDefaults(Notification.DEFAULT_SOUND | Notification.DEFAULT_VIBRATE)
                .setAutoCancel(true)//点击后取消
                .setWhen(System.currentTimeMillis())//设置通知时间
                .setPriority(Notification.PRIORITY_HIGH)//高优先级
                .setVisibility(Notification.VISIBILITY_PRIVATE)
                //android5.0加入了一种新的模式Notification的显示等级，共有三种：
                //VISIBILITY_PUBLIC  只有在没有锁屏时会显示通知
                //VISIBILITY_PRIVATE 任何情况都会显示通知
                //VISIBILITY_SECRET  在安全锁和没有锁屏的情况下显示通知
                .setContentIntent(pi);
        Notification myNotification = myBuilder.build();

        //4.通过通知管理器来发起通知，ID区分通知
        myManager.notify(NOTIFICATION_ID_1, myNotification);
    }

    private void init(String url){
        webView = (WebView) findViewById(R.id.webView);
        //WebView加载web资源
        webView.loadUrl("http://" + url + ":8080/?action=stream");
        //覆盖WebView默认使用第三方或系统默认浏览器打开网页的行为，使网页用WebView打开
        webView.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                // TODO Auto-generated method stub
                //返回值是true的时候控制去WebView打开，为false调用系统浏览器或第三方浏览器
                view.loadUrl(url);
                return true;
            }
        });

    }

    Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);  //返回父级的message，不知道什么作用
            // TODO
            // UI界面的更新等相关操作
            tongzhilan();
            Bundle data = msg.getData();
            String val = data.getString("value");
            byte b[]= Base64.decode(val,Base64.DEFAULT);
            bitmap = BitmapFactory.decodeByteArray(b, 0, b.length);
            tanchu();
        }
    };

    public void tanchu() {
        final ImageView inputServer = new ImageView(mContext);
        inputServer.setImageBitmap(bitmap);
        AlertDialog.Builder builder = new AlertDialog.Builder(mContext);
        builder.setTitle(" ").setView(inputServer)
                .setNegativeButton("确定", null);
        builder.show();
    }

    Runnable socketRun = new Runnable() {

        @Override
        public void run() {
            // TODO Auto-generated method stub
            int SERVER_PORT = 12462;
            try {
                System.out.println("Server: Connecting...");
                ServerSocket serverSocket = new ServerSocket(SERVER_PORT);    //接收
                while (true) {
                    //循环监听客户端请求
                    Socket clientSocket = serverSocket.accept();
                    System.out.println("Server: Receiving...");
                    try {
                        BufferedReader in = new BufferedReader(
                                new InputStreamReader(clientSocket.getInputStream()));
                        //获取从客户端发来的信息
                        String str = in.readLine();
                        System.out.println("输出: '" + str + "'");
                        Message msg = new Message();
                        Bundle data1 = new Bundle();  //键值对
                        data1.putString("value", str);
                        msg.setData(data1);
                        handler.sendMessage(msg);
                    } catch (Exception e) {
                        System.out.println("Server: Error");
                        e.printStackTrace();
                    } finally {
                        clientSocket.close();
                        System.out.println("Server: Close.");
                        System.gc();
                    }
                }

            } catch (Exception e) {
                System.out.println("Server: Error");
                e.printStackTrace();
            }
        }
    };

    Runnable send = new Runnable() {

        @Override
        public void run() {
            // TODO Auto-generated method stub
            int SERVER_PORT = 12462;
            try {
                System.out.println("Client：Connecting");
                //IP地址和端口号（对应服务端），我这的IP是本地路由器的IP地址
                Socket socket = new Socket(url, SERVER_PORT);
                //发送给服务端的消息
                String message = "1";
                try {
                    System.out.println("Client Sending: '" + message + "'");

                    //第二个参数为True则为自动flush
                    PrintWriter out = new PrintWriter(
                            new BufferedWriter(new OutputStreamWriter(
                                    socket.getOutputStream())), true);
                    out.println(message);
//                      out.flush();
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    //关闭Socket
                    socket.close();
                    System.out.println("Client:Socket closed");
                }
            } catch (UnknownHostException e1) {
                e1.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    };

}
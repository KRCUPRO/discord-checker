package com.krcupro.discordchecker;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.PowerManager;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.DownloadListener;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;

public class MainActivity extends Activity {
    private static final String PREFS_NAME = "D4UC_PREFS";
    private static final String KEY_SERVER_URL = "server_url";
    private static final String DEFAULT_EMULATOR_URL = "http://10.0.2.2:5000";

    private WebView webView;
    private PowerManager.WakeLock wakeLock;
    private SharedPreferences prefs;

    public static boolean isEmulator() {
        return Build.FINGERPRINT.startsWith("generic")
            || Build.FINGERPRINT.startsWith("unknown")
            || Build.MODEL.contains("google_sdk")
            || Build.MODEL.contains("Emulator")
            || Build.MODEL.contains("Android SDK built for x86")
            || Build.MANUFACTURER.contains("Genymotion")
            || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
            || "google_sdk".equals(Build.PRODUCT);
    }

    public static String getDeviceLocalIp() {
        try {
            Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces();
            String fallbackIp = "";
            while (en != null && en.hasMoreElements()) {
                NetworkInterface intf = en.nextElement();
                String name = intf.getName() != null ? intf.getName().toLowerCase() : "";
                boolean isWifiOrEth = name.startsWith("wlan") || name.startsWith("eth") || name.contains("wlan");
                Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses();
                while (enumIpAddr.hasMoreElements()) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && (inetAddress instanceof Inet4Address)) {
                        String ip = inetAddress.getHostAddress();
                        if (ip != null && !ip.startsWith("127.") && !ip.startsWith("169.254.")) {
                            if (isWifiOrEth) {
                                return ip; // Prioritize local Wi-Fi / Ethernet over cellular
                            }
                            if (fallbackIp.isEmpty()) {
                                fallbackIp = ip;
                            }
                        }
                    }
                }
            }
            if (!fallbackIp.isEmpty()) {
                return fallbackIp;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "";
    }

    public static String getDeviceModel() {
        return Build.MANUFACTURER + " " + Build.MODEL;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Discord dark theme status bar & navigation bar
        Window window = getWindow();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
            window.setStatusBarColor(Color.parseColor("#1e1f22"));
            window.setNavigationBarColor(Color.parseColor("#1e1f22"));
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            try {
                WindowManager.LayoutParams lp = window.getAttributes();
                lp.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
                window.setAttributes(lp);
            } catch (Exception e) {}
        }

        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);

        webView = new WebView(this);
        webView.setBackgroundColor(Color.parseColor("#1e1f22"));
        setContentView(webView);

        initWebView();
        loadApp();

        if (!prefs.contains(KEY_SERVER_URL)) {
            Toast.makeText(this, "📱 PC에서 D4UC Web 실행 후, 설정 탭에서 PC IP(포트 5000)를 입력하세요.", Toast.LENGTH_LONG).show();
        }
    }

    private void initWebView() {
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage cm) {
                return super.onConsoleMessage(cm);
            }
        });

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                if (url != null && (url.startsWith("http://") || url.startsWith("https://"))) {
                    if (url.contains("/api/export")) {
                        try {
                            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                            startActivity(intent);
                            return true;
                        } catch (Exception e) {
                            // Fallback to WebView
                        }
                    }
                }
                view.loadUrl(url);
                return true;
            }
        });

        webView.setDownloadListener(new DownloadListener() {
            @Override
            public void onDownloadStart(String url, String userAgent, String contentDisposition, String mimetype, long contentLength) {
                try {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    intent.setData(Uri.parse(url));
                    startActivity(intent);
                } catch (Exception e) {
                    Toast.makeText(MainActivity.this, "다운로드 요청 실패: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                }
            }
        });

        webView.addJavascriptInterface(new AndroidBridge(this), "AndroidBridge");
    }

    public void loadApp() {
        webView.loadUrl("file:///android_asset/www/index.html");
    }

    public String getServerUrl() {
        if (prefs.contains(KEY_SERVER_URL)) {
            String url = prefs.getString(KEY_SERVER_URL, "");
            if (!isEmulator() && url != null && url.contains("10.0.2.2")) {
                prefs.edit().remove(KEY_SERVER_URL).apply();
                return "";
            }
            return url;
        }
        if (isEmulator()) {
            return DEFAULT_EMULATOR_URL;
        }
        return "";
    }

    public void setServerUrl(String url) {
        prefs.edit().putString(KEY_SERVER_URL, url).apply();
    }

    public void setWakeLock(final boolean enable) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                try {
                    if (enable) {
                        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                        if (wakeLock == null) {
                            PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
                            if (pm != null) {
                                wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "D4UC::KeepAwake");
                            }
                        }
                        if (wakeLock != null && !wakeLock.isHeld()) {
                            wakeLock.acquire();
                        }
                    } else {
                        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                        if (wakeLock != null && wakeLock.isHeld()) {
                            wakeLock.release();
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void showServerUrlDialog() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (isFinishing() || (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1 && isDestroyed())) {
                    return;
                }
                AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                builder.setTitle("🌐 D4UC 서버 주소 설정 / Server URL");
                builder.setMessage("PC 또는 원격 서버의 D4UC Web 서버 주소를 입력하세요.\n(예: http://192.168.0.10:5000 또는 http://10.0.2.2:5000)");

                final EditText input = new EditText(MainActivity.this);
                input.setText(getServerUrl());
                input.setSingleLine(true);
                LinearLayout container = new LinearLayout(MainActivity.this);
                container.setOrientation(LinearLayout.VERTICAL);
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
                lp.setMargins(40, 20, 40, 20);
                input.setLayoutParams(lp);
                container.addView(input);
                builder.setView(container);

                builder.setPositiveButton("저장 및 연결 (Save)", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String newUrl = input.getText().toString().trim();
                        if (!newUrl.isEmpty()) {
                            if (!newUrl.startsWith("http://") && !newUrl.startsWith("https://")) {
                                newUrl = "http://" + newUrl;
                            }
                            while (newUrl.endsWith("/")) {
                                newUrl = newUrl.substring(0, newUrl.length() - 1);
                            }
                            // Auto-append default port 5000 if port omitted
                            int colonIdx = newUrl.indexOf(':', 7);
                            if (colonIdx == -1) {
                                newUrl = newUrl + ":5000";
                            }
                            setServerUrl(newUrl);
                            Toast.makeText(MainActivity.this, "서버 주소 설정됨: " + newUrl, Toast.LENGTH_SHORT).show();
                            webView.loadUrl("javascript:(function(){ if(window.setServerUrlFromNative) window.setServerUrlFromNative('" + newUrl + "'); else location.reload(); })()");
                        }
                    }
                });

                builder.setNegativeButton("취소 (Cancel)", null);
                builder.show();
            }
        });
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        setWakeLock(false);
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }
}

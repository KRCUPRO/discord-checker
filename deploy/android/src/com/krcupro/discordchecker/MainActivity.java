package com.krcupro.discordchecker;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.PowerManager;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;

public class MainActivity extends Activity {
    private static final String PREFS_NAME = "D4UC_PREFS";
    private static final String KEY_SERVER_URL = "server_url";
    private static final String DEFAULT_SERVER_URL = "http://127.0.0.1:8080";

    private WebView webView;
    private PowerManager.WakeLock wakeLock;
    private SharedPreferences prefs;

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

        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);

        webView = new WebView(this);
        webView.setBackgroundColor(Color.parseColor("#1e1f22"));
        setContentView(webView);

        initWebView();
        loadApp();
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
                view.loadUrl(url);
                return true;
            }
        });

        webView.addJavascriptInterface(new AndroidBridge(this), "AndroidBridge");
    }

    public void loadApp() {
        webView.loadUrl("file:///android_asset/www/index.html");
    }

    public String getServerUrl() {
        return prefs.getString(KEY_SERVER_URL, DEFAULT_SERVER_URL);
    }

    public void setServerUrl(String url) {
        prefs.edit().putString(KEY_SERVER_URL, url).apply();
    }

    public void setWakeLock(boolean enable) {
        try {
            if (enable) {
                if (wakeLock == null) {
                    PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
                    wakeLock = pm.newWakeLock(PowerManager.SCREEN_BRIGHT_WAKE_LOCK | PowerManager.ON_AFTER_RELEASE, "D4UC::WakeLock");
                }
                if (!wakeLock.isHeld()) {
                    wakeLock.acquire();
                }
            } else {
                if (wakeLock != null && wakeLock.isHeld()) {
                    wakeLock.release();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void showServerUrlDialog() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                builder.setTitle("🌐 D4UC 서버 주소 설정 / Server URL");
                builder.setMessage("PC 또는 원격 서버의 D4UC Web 서버 주소를 입력하세요.\n(예: http://192.168.0.10:8080 또는 http://10.0.2.2:8080)");

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

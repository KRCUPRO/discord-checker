package com.krcupro.discordchecker;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.webkit.JavascriptInterface;
import android.widget.Toast;

public class AndroidBridge {
    private final MainActivity activity;

    public AndroidBridge(MainActivity activity) {
        this.activity = activity;
    }

    @JavascriptInterface
    public void copyToClipboard(final String text) {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                try {
                    ClipboardManager cm = (ClipboardManager) activity.getSystemService(Context.CLIPBOARD_SERVICE);
                    ClipData clip = ClipData.newPlainText("D4UC Username", text);
                    if (cm != null) {
                        cm.setPrimaryClip(clip);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }

    @JavascriptInterface
    public void showToast(final String message) {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                Toast.makeText(activity, message, Toast.LENGTH_SHORT).show();
            }
        });
    }

    @JavascriptInterface
    public void setWakeLock(final boolean enabled) {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.setWakeLock(enabled);
            }
        });
    }

    @JavascriptInterface
    public String getServerUrl() {
        return activity.getServerUrl();
    }

    @JavascriptInterface
    public void setServerUrl(final String url) {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.setServerUrl(url);
            }
        });
    }

    @JavascriptInterface
    public void openServerConfigDialog() {
        activity.showServerUrlDialog();
    }

    @JavascriptInterface
    public boolean isAndroidApp() {
        return true;
    }

    @JavascriptInterface
    public String getAppVersion() {
        return "v12.3.0";
    }
}

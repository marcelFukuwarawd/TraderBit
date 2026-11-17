```python
import os

FILES = {
    "settings.gradle.kts": r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "BTCTraderSim"
include(":app")
''',

    "build.gradle.kts": r'''plugins {
    id("com.android.application") version "8.7.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
''',

    "gradle.properties": r'''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
''',

    "app/build.gradle.kts": r'''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.btcsim.trader"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.btcsim.trader"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            isShrinkResources = false
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.10.01")
    implementation(composeBom)

    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.6")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")

    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("androidx.work:work-runtime-ktx:2.9.1")
}
''',

    "app/src/main/AndroidManifest.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

    <application
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher"
        android:roundIcon="@drawable/ic_launcher"
        android:label="BTC Trader Sim"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.NoActionBar">

        <activity
            android:name=".ui.MainActivity"
            android:exported="true"
            android:launchMode="singleTop">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.TradingForegroundService"
            android:enabled="true"
            android:exported="false"
            android:foregroundServiceType="dataSync" />

        <receiver
            android:name=".service.BootReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>

        <receiver
            android:name=".widget.BtcWidgetProvider"
            android:exported="true"
            android:label="BTC/USDT Auto Trader (5x5)">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
                <action android:name="com.btcsim.trader.ACTION_TOGGLE_BOT" />
                <action android:name="com.btcsim.trader.ACTION_REFRESH_WIDGET" />
            </intent-filter>

            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/widget_btc_trader_info" />
        </receiver>
    </application>
</manifest>
''',

    "app/src/main/res/drawable/ic_launcher_bg.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0B0E11"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="#181A20"
        android:pathData="M54,10 A44,44 0 1,1 53.99,10 Z" />
</vector>
''',

    "app/src/main/res/drawable/ic_launcher_fg.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#FCD535"
        android:pathData="M24,68 L42,50 L54,60 L78,34 L84,40 L55,71 L43,61 L30,74 Z" />
    <path
        android:fillColor="#0ECB81"
        android:pathData="M67,34 L84,34 L84,51 L78,51 L78,40 L67,40 Z" />
    <path
        android:fillColor="#0ECB81"
        android:pathData="M34,74 h6 v8 h-6 z" />
    <path
        android:fillColor="#F6465D"
        android:pathData="M48,70 h6 v12 h-6 z" />
    <path
        android:fillColor="#0ECB81"
        android:pathData="M62,60 h6 v22 h-6 z" />
    <path
        android:fillColor="#0ECB81"
        android:pathData="M76,54 h6 v28 h-6 z" />
</vector>
''',

    "app/src/main/res/drawable/ic_launcher.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="48dp"
    android:height="48dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0B0E11"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="#FCD535"
        android:pathData="M22,68 L40,50 L52,60 L78,32 L85,39 L53,72 L41,62 L29,75 Z" />
    <path
        android:fillColor="#0ECB81"
        android:pathData="M66,32 L85,32 L85,51 L78,51 L78,39 L66,39 Z" />
</vector>
''',

    "app/src/main/res/drawable-v26/ic_launcher.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_bg" />
    <foreground android:drawable="@drawable/ic_launcher_fg" />
</adaptive-icon>
''',

    "app/src/main/res/drawable/ic_notif_btc.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M3.5,18.5 L9.5,12.5 L13.5,16.5 L20.5,8.5 L22,10 L13.5,19.5 L9.5,15.5 L5,20 Z" />
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M16,7 L22,7 L22,13 L20,13 L20,9 L16,9 Z" />
</vector>
''',

    "app/src/main/res/drawable/widget_bg.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#0B0E11" />
    <corners android:radius="18dp" />
    <stroke android:width="1dp" android:color="#2B3139" />
</shape>
''',

    "app/src/main/res/drawable/widget_card_bg.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#181A20" />
    <corners android:radius="12dp" />
</shape>
''',

    "app/src/main/res/drawable/badge_green.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#1A0ECB81" />
    <corners android:radius="6dp" />
    <stroke android:width="1dp" android:color="#0ECB81" />
</shape>
''',

    "app/src/main/res/drawable/badge_red.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#1AF6465D" />
    <corners android:radius="6dp" />
    <stroke android:width="1dp" android:color="#F6465D" />
</shape>
''',

    "app/src/main/res/drawable/badge_gold.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#1AFCD535" />
    <corners android:radius="6dp" />
    <stroke android:width="1dp" android:color="#FCD535" />
</shape>
''',

    "app/src/main/res/drawable/btn_gold.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FCD535" />
    <corners android:radius="8dp" />
</shape>
''',

    "app/src/main/res/drawable/btn_dark.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#2B3139" />
    <corners android:radius="8dp" />
</shape>
''',

    "app/src/main/res/xml/widget_btc_trader_info.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="320dp"
    android:minHeight="320dp"
    android:targetCellWidth="5"
    android:targetCellHeight="5"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_btc_trader_5x5"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen" />
''',

    "app/src/main/res/layout/widget_btc_trader_5x5.xml": r'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@drawable/widget_bg"
    android:orientation="vertical"
    android:padding="12dp">

    <!-- Cabecalho -->
    <LinearLayout
        android:id="@+id/widget_header"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="center_vertical"
        android:orientation="horizontal">

        <LinearLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:orientation="vertical">

            <LinearLayout
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:gravity="center_vertical"
                android:orientation="horizontal">

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="BTC/USDT • SPOT 1x"
                    android:textColor="#EAECEF"
                    android:textSize="12sp"
                    android:textStyle="bold" />

                <TextView
                    android:id="@+id/w_profile_badge"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginStart="6dp"
                    android:background="@drawable/badge_gold"
                    android:paddingLeft="5dp"
                    android:paddingTop="1dp"
                    android:paddingRight="5dp"
                    android:paddingBottom="1dp"
                    android:text="5M"
                    android:textColor="#FCD535"
                    android:textSize="9sp"
                    android:textStyle="bold" />
            </LinearLayout>

            <TextView
                android:id="@+id/w_btc_price"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="2dp"
                android:text="$ --,--"
                android:textColor="#FFFFFF"
                android:textSize="22sp"
                android:textStyle="bold" />
        </LinearLayout>

        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:gravity="end"
            android:orientation="vertical">

            <TextView
                android:id="@+id/w_bot_badge"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:background="@drawable/badge_red"
                android:paddingLeft="8dp"
                android:paddingTop="3dp"
                android:paddingRight="8dp"
                android:paddingBottom="3dp"
                android:text="PAUSADO"
                android:textColor="#F6465D"
                android:textSize="10sp"
                android:textStyle="bold" />

            <TextView
                android:id="@+id/w_change_24h"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="4dp"
                android:text="24h: 0.00%"
                android:textColor="#0ECB81"
                android:textSize="12sp"
                android:textStyle="bold" />
        </LinearLayout>
    </LinearLayout>

    <!-- Painel de Capital -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="9dp"
        android:background="@drawable/widget_card_bg"
        android:orientation="horizontal"
        android:padding="10dp">

        <LinearLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:orientation="vertical">
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="CAIXA DIA"
                android:textColor="#848E9C"
                android:textSize="9sp" />
            <TextView
                android:id="@+id/w_initial_box"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="$100.00"
                android:textColor="#EAECEF"
                android:textSize="13sp"
                android:textStyle="bold" />
        </LinearLayout>

        <LinearLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:orientation="vertical">
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="PATRIMONIO"
                android:textColor="#848E9C"
                android:textSize="9sp" />
            <TextView
                android:id="@+id/w_equity"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="$100.00"
                android:textColor="#FFFFFF"
                android:textSize="13sp"
                android:textStyle="bold" />
        </LinearLayout>

        <LinearLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1.2"
            android:gravity="end"
            android:orientation="vertical">
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="RESULTADO DIA"
                android:textColor="#848E9C"
                android:textSize="9sp" />
            <TextView
                android:id="@+id/w_daily_pnl"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="+$0.00 (0.0%)"
                android:textColor="#0ECB81"
                android:textSize="13sp"
                android:textStyle="bold" />
        </LinearLayout>
    </LinearLayout>

    <!-- Posicao Ativa e Radar -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:background="@drawable/widget_card_bg"
        android:orientation="vertical"
        android:padding="10dp">

        <TextView
            android:id="@+id/w_pos_title"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:ellipsize="end"
            android:maxLines="1"
            android:text="POSICAO: AGUARDANDO SINAL"
            android:textColor="#FCD535"
            android:textSize="11sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/w_pos_details"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="3dp"
            android:ellipsize="end"
            android:maxLines="1"
            android:text="Entrada: -- | SL: -- | TP: --"
            android:textColor="#EAECEF"
            android:textSize="11sp" />

        <TextView
            android:id="@+id/w_indicators"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="5dp"
            android:ellipsize="end"
            android:maxLines="1"
            android:text="EMA: -- | RSI: -- | MACD: -- | ATR: --"
            android:textColor="#848E9C"
            android:textSize="10sp" />
    </LinearLayout>

    <!-- Trades do Dia e Relatorio 21h -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_marginTop="8dp"
        android:layout_weight="1"
        android:background="@drawable/widget_card_bg"
        android:orientation="vertical"
        android:padding="10dp">

        <TextView
            android:id="@+id/w_trades_header"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="TRADES HOJE: 0 • FECHAMENTO 21H"
            android:textColor="#848E9C"
            android:textSize="10sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/w_recent_trades"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"
            android:ellipsize="end"
            android:lineSpacingExtra="2dp"
            android:maxLines="4"
            android:text="Nenhuma operacao encerrada hoje."
            android:textColor="#EAECEF"
            android:textSize="11sp" />
    </LinearLayout>

    <!-- Botoes Rapidos -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:gravity="center_vertical"
        android:orientation="horizontal">

        <TextView
            android:id="@+id/w_btn_toggle"
            android:layout_width="0dp"
            android:layout_height="34dp"
            android:layout_weight="1"
            android:background="@drawable/btn_gold"
            android:gravity="center"
            android:text="INICIAR BOT"
            android:textColor="#0B0E11"
            android:textSize="11sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/w_btn_refresh"
            android:layout_width="wrap_content"
            android:layout_height="34dp"
            android:layout_marginStart="8dp"
            android:background="@drawable/btn_dark"
            android:gravity="center"
            android:paddingLeft="14dp"
            android:paddingRight="14dp"
            android:text="ATUALIZAR"
            android:textColor="#EAECEF"
            android:textSize="10sp"
            android:textStyle="bold" />
    </LinearLayout>
</LinearLayout>
''',

    "app/src/main/java/com/btcsim/trader/model/TradingModels.kt": r'''package com.btcsim.trader.model

enum class TradingProfile(
    val id: String,
    val label: String,
    val shortBadge: String,
    val interval: String,
    val description: String
) {
    DAY_5M(
        id = "DAY_5M",
        label = "Day Trade 5m",
        shortBadge = "5M",
        interval = "5m",
        description = "Alta frequencia intraday: EMA 9/21/50 + RSI + Volume + Bollinger"
    ),
    DAY_15M(
        id = "DAY_15M",
        label = "Day Trade 15m",
        shortBadge = "15M",
        interval = "15m",
        description = "Equilibrio ideal: menos ruido de mercado e alvos maiores"
    ),
    SWING_1H(
        id = "SWING_1H",
        label = "Swing Trade 1h",
        shortBadge = "1H",
        interval = "1h",
        description = "Tendencias mais longas com MACD e Trailing Stop ampliado"
    );

    companion object {
        fun fromId(id: String?): TradingProfile =
            entries.firstOrNull { it.id == id } ?: DAY_5M
    }
}

data class BotSettings(
    val profile: TradingProfile = TradingProfile.DAY_5M,
    val resetDailyCapital: Boolean = true,
    val dailyMaxLossPercent: Double = 3.0,
    val soundAlertsEnabled: Boolean = true
)

data class Candle(
    val openTime: Long,
    val open: Double,
    val high: Double,
    val low: Double,
    val close: Double,
    val volume: Double
)

data class IndicatorSnapshot(
    val price: Double = 0.0,
    val ema9: Double = 0.0,
    val ema21: Double = 0.0,
    val ema50: Double = 0.0,
    val rsi: Double = 50.0,
    val prevRsi: Double = 50.0,
    val macdLine: Double = 0.0,
    val macdSignal: Double = 0.0,
    val macdHist: Double = 0.0,
    val prevMacdHist: Double = 0.0,
    val bbUpper: Double = 0.0,
    val bbMiddle: Double = 0.0,
    val bbLower: Double = 0.0,
    val atr: Double = 0.0,
    val volumeRatio: Double = 1.0,
    val signalText: String = "Aguardando dados..."
)

data class OpenPosition(
    val entryPrice: Double,
    val btcQty: Double,
    val investedUsdt: Double,
    val entryFeeUsdt: Double,
    val stopLoss: Double,
    val takeProfit: Double,
    val trailingActive: Boolean = false,
    val setupName: String,
    val profileLabel: String,
    val entryTime: Long
) {
    fun currentValueUsdt(currentPrice: Double): Double = btcQty * currentPrice

    fun unrealizedPnl(currentPrice: Double, feeRate: Double = 0.001): Double {
        val grossExit = btcQty * currentPrice
        val estimatedExitFee = grossExit * feeRate
        return (grossExit - estimatedExitFee) - investedUsdt
    }

    fun unrealizedPnlPercent(currentPrice: Double, feeRate: Double = 0.001): Double {
        if (investedUsdt <= 0.0) return 0.0
        return (unrealizedPnl(currentPrice, feeRate) / investedUsdt) * 100.0
    }
}

data class CompletedTrade(
    val id: String,
    val setupName: String,
    val entryPrice: Double,
    val exitPrice: Double,
    val btcQty: Double,
    val grossPnl: Double,
    val totalFees: Double,
    val netPnl: Double,
    val pnlPercent: Double,
    val exitReason: String,
    val entryTime: Long,
    val exitTime: Long
)

data class DailyReport(
    val date: String,
    val initialBalance: Double,
    val finalBalance: Double,
    val totalGains: Double,
    val totalLosses: Double,
    val totalFees: Double,
    val netPnl: Double,
    val netPnlPercent: Double,
    val totalTrades: Int,
    val winningTrades: Int,
    val losingTrades: Int,
    val bestTradePnl: Double,
    val worstTradePnl: Double,
    val generatedAt: Long
)

data class SimulationState(
    val isBotRunning: Boolean = false,
    val settings: BotSettings = BotSettings(),
    val initialDailyBalance: Double = 100.0,
    val availableUsdt: Double = 100.0,
    val openPosition: OpenPosition? = null,
    val todayTrades: List<CompletedTrade> = emptyList(),
    val dailyReports: List<DailyReport> = emptyList(),
    val recentCandles: List<Candle> = emptyList(),
    val lastPrice: Double = 0.0,
    val priceChange24hPercent: Double = 0.0,
    val high24h: Double = 0.0,
    val low24h: Double = 0.0,
    val lastIndicators: IndicatorSnapshot? = null,
    val lastReportDate: String = "",
    val lastUpdated: Long = 0L,
    val statusMessage: String = "Pronto para operar ($100.00 Spot 1x)"
) {
    fun totalEquity(): Double {
        val posVal = if (openPosition != null && lastPrice > 0.0) {
            openPosition.currentValueUsdt(lastPrice)
        } else {
            0.0
        }
        return availableUsdt + posVal
    }

    fun todayRealizedPnl(): Double = todayTrades.sumOf { it.netPnl }

    fun todayGains(): Double = todayTrades.filter { it.netPnl > 0.0 }.sumOf { it.netPnl }

    fun todayLosses(): Double = todayTrades.filter { it.netPnl < 0.0 }.sumOf { it.netPnl }

    fun todayFees(): Double = todayTrades.sumOf { it.totalFees }

    fun todayTotalPnl(): Double = totalEquity() - initialDailyBalance

    fun todayTotalPnlPercent(): Double {
        if (initialDailyBalance <= 0.0) return 0.0
        return (todayTotalPnl() / initialDailyBalance) * 100.0
    }
}
''',

    "app/src/main/java/com/btcsim/trader/strategy/Indicators.kt": r'''package com.btcsim.trader.strategy

import com.btcsim.trader.model.Candle
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.pow
import kotlin.math.sqrt

object Indicators {

    data class BollingerBand(val upper: Double, val middle: Double, val lower: Double)

    data class MacdResult(
        val macdLine: Double,
        val signalLine: Double,
        val histogram: Double,
        val prevHistogram: Double
    )

    fun calculateEmaSeries(values: List<Double>, period: Int): List<Double> {
        if (values.isEmpty() || period <= 0) return emptyList()
        if (values.size < period) {
            val avg = values.average()
            return List(values.size) { avg }
        }
        val k = 2.0 / (period + 1.0)
        val result = MutableList(values.size) { 0.0 }
        var ema = values.take(period).average()
        for (i in 0 until period) {
            result[i] = ema
        }
        for (i in period until values.size) {
            ema = (values[i] * k) + (ema * (1.0 - k))
            result[i] = ema
        }
        return result
    }

    fun calculateRsiSeries(closes: List<Double>, period: Int = 14): List<Double> {
        if (closes.isEmpty()) return emptyList()
        if (closes.size <= period) return List(closes.size) { 50.0 }

        val result = MutableList(closes.size) { 50.0 }
        var gainSum = 0.0
        var lossSum = 0.0

        for (i in 1..period) {
            val delta = closes[i] - closes[i - 1]
            if (delta >= 0.0) gainSum += delta else lossSum += abs(delta)
        }

        var avgGain = gainSum / period
        var avgLoss = lossSum / period
        result[period] = computeRsi(avgGain, avgLoss)

        for (i in (period + 1) until closes.size) {
            val delta = closes[i] - closes[i - 1]
            val gain = if (delta > 0.0) delta else 0.0
            val loss = if (delta < 0.0) abs(delta) else 0.0
            avgGain = ((avgGain * (period - 1)) + gain) / period
            avgLoss = ((avgLoss * (period - 1)) + loss) / period
            result[i] = computeRsi(avgGain, avgLoss)
        }
        return result
    }

    private fun computeRsi(avgGain: Double, avgLoss: Double): Double {
        if (avgLoss == 0.0) return 100.0
        val rs = avgGain / avgLoss
        return 100.0 - (100.0 / (1.0 + rs))
    }

    fun calculateMacd(closes: List<Double>): MacdResult {
        if (closes.size < 36) return MacdResult(0.0, 0.0, 0.0, 0.0)
        val ema12 = calculateEmaSeries(closes, 12)
        val ema26 = calculateEmaSeries(closes, 26)
        val macdSeries = List(closes.size) { i -> ema12[i] - ema26[i] }
        val signalSeries = calculateEmaSeries(macdSeries, 9)

        val lastIdx = closes.size - 1
        val prevIdx = closes.size - 2
        val lastMacd = macdSeries[lastIdx]
        val lastSig = signalSeries[lastIdx]
        val lastHist = lastMacd - lastSig
        val prevHist = macdSeries[prevIdx] - signalSeries[prevIdx]

        return MacdResult(
            macdLine = lastMacd,
            signalLine = lastSig,
            histogram = lastHist,
            prevHistogram = prevHist
        )
    }

    fun calculateBollingerBands(
        closes: List<Double>,
        period: Int = 20,
        stdDevMult: Double = 2.0
    ): BollingerBand {
        if (closes.size < period) {
            val last = closes.lastOrNull() ?: 0.0
            return BollingerBand(last, last, last)
        }
        val window = closes.takeLast(period)
        val mean = window.average()
        val variance = window.sumOf { (it - mean).pow(2) } / period
        val stdDev = sqrt(variance)
        return BollingerBand(
            upper = mean + stdDevMult * stdDev,
            middle = mean,
            lower = mean - stdDevMult * stdDev
        )
    }

    fun calculateBollingerSeries(
        closes: List<Double>,
        period: Int = 20,
        stdDevMult: Double = 2.0
    ): Pair<List<Double>, List<Double>> {
        val uppers = MutableList(closes.size) { 0.0 }
        val lowers = MutableList(closes.size) { 0.0 }
        for (i in closes.indices) {
            val start = max(0, i - period + 1)
            val slice = closes.subList(start, i + 1)
            val mean = slice.average()
            val variance = slice.sumOf { (it - mean).pow(2) } / slice.size
            val stdDev = sqrt(variance)
            uppers[i] = mean + stdDevMult * stdDev
            lowers[i] = mean - stdDevMult * stdDev
        }
        return Pair(uppers, lowers)
    }

    fun calculateAtr(candles: List<Candle>, period: Int = 14): Double {
        if (candles.size <= period) return 0.0
        val trueRanges = mutableListOf<Double>()
        for (i in 1 until candles.size) {
            val curr = candles[i]
            val prevClose = candles[i - 1].close
            val tr = max(
                curr.high - curr.low,
                max(abs(curr.high - prevClose), abs(curr.low - prevClose))
            )
            trueRanges.add(tr)
        }
        if (trueRanges.size < period) return 0.0
        var atr = trueRanges.take(period).average()
        for (i in period until trueRanges.size) {
            atr = ((atr * (period - 1)) + trueRanges[i]) / period
        }
        return atr
    }

    fun calculateVolumeRatio(candles: List<Candle>, period: Int = 20): Double {
        if (candles.size < period + 2) return 1.0
        val closedCandle = candles[candles.size - 2]
        val prevVolumes = candles.subList(candles.size - 2 - period, candles.size - 2).map { it.volume }
        val avgVol = prevVolumes.average()
        return if (avgVol > 0.0) closedCandle.volume / avgVol else 1.0
    }
}
''',

    "app/src/main/java/com/btcsim/trader/strategy/TradingEngine.kt": r'''package com.btcsim.trader.strategy

import com.btcsim.trader.model.*
import java.text.SimpleDateFormat
import java.util.*
import kotlin.math.max

object TradingEngine {

    const val INITIAL_DAILY_CAPITAL = 100.0
    const val SPOT_FEE_RATE = 0.001 // 0.1% taxa padrao Spot Binance

    data class EngineResult(
        val newState: SimulationState,
        val tradeNotification: String? = null,
        val generatedReport: DailyReport? = null
    )

    private data class ProfileParams(
        val minRiskPct: Double,
        val minRewardPct: Double,
        val atrStopMult: Double,
        val atrTargetMult: Double,
        val trailingTriggerPct: Double
    )

    private fun paramsFor(profile: TradingProfile): ProfileParams = when (profile) {
        TradingProfile.DAY_5M -> ProfileParams(
            minRiskPct = 0.006,
            minRewardPct = 0.012,
            atrStopMult = 1.5,
            atrTargetMult = 3.0,
            trailingTriggerPct = 0.0075
        )
        TradingProfile.DAY_15M -> ProfileParams(
            minRiskPct = 0.008,
            minRewardPct = 0.016,
            atrStopMult = 1.6,
            atrTargetMult = 3.2,
            trailingTriggerPct = 0.0095
        )
        TradingProfile.SWING_1H -> ProfileParams(
            minRiskPct = 0.012,
            minRewardPct = 0.025,
            atrStopMult = 1.8,
            atrTargetMult = 3.8,
            trailingTriggerPct = 0.014
        )
    }

    fun processMarketTick(
        currentState: SimulationState,
        candles: List<Candle>,
        livePrice: Double,
        change24hPercent: Double,
        high24h: Double,
        low24h: Double,
        nowMillis: Long = System.currentTimeMillis()
    ): EngineResult {
        if (candles.size < 60 || livePrice <= 0.0) {
            return EngineResult(
                currentState.copy(
                    lastPrice = if (livePrice > 0.0) livePrice else currentState.lastPrice,
                    priceChange24hPercent = change24hPercent,
                    high24h = if (high24h > 0.0) high24h else currentState.high24h,
                    low24h = if (low24h > 0.0) low24h else currentState.low24h,
                    lastUpdated = nowMillis,
                    statusMessage = "Sincronizando historico de candles..."
                )
            )
        }

        // 1. Consolidacao automatica do relatorio diario as 21h
        val cal = Calendar.getInstance().apply { timeInMillis = nowMillis }
        val todayStr = formatDateKey(nowMillis)
        if (cal.get(Calendar.HOUR_OF_DAY) >= 21 && currentState.lastReportDate != todayStr) {
            return generateDailyReport(
                state = currentState.copy(
                    lastPrice = livePrice,
                    priceChange24hPercent = change24hPercent,
                    high24h = high24h,
                    low24h = low24h,
                    recentCandles = candles.takeLast(60)
                ),
                nowMillis = nowMillis,
                resetForNextDay = true
            )
        }

        // 2. Calculo de todos os indicadores sobre candles fechados
        val closes = candles.map { it.close }
        val closedIdx = candles.size - 2
        val prevIdx = candles.size - 3
        val closedSlice = closes.subList(0, closedIdx + 1)
        val closedCandles = candles.subList(0, closedIdx + 1)

        val ema9List = Indicators.calculateEmaSeries(closedSlice, 9)
        val ema21List = Indicators.calculateEmaSeries(closedSlice, 21)
        val ema50List = Indicators.calculateEmaSeries(closedSlice, 50)
        val rsiList = Indicators.calculateRsiSeries(closedSlice, 14)
        val macd = Indicators.calculateMacd(closedSlice)
        val bb = Indicators.calculateBollingerBands(closedSlice, 20, 2.0)
        val atr = Indicators.calculateAtr(closedCandles, 14)
        val volRatio = Indicators.calculateVolumeRatio(candles, 20)

        val closedCandle = candles[closedIdx]
        val prevCandle = candles[prevIdx]
        val ema9 = ema9List.last()
        val ema21 = ema21List.last()
        val ema50 = ema50List.last()
        val rsi = rsiList.last()
        val prevRsi = rsiList[rsiList.size - 2]
        val prevHigh10 = candles.subList(closedIdx - 10, closedIdx).maxOf { it.high }

        val p = paramsFor(currentState.settings.profile)

        var state = currentState.copy(
            lastPrice = livePrice,
            priceChange24hPercent = change24hPercent,
            high24h = high24h,
            low24h = low24h,
            recentCandles = candles.takeLast(60),
            lastUpdated = nowMillis
        )

        var tradeAlert: String? = null
        val activePos = state.openPosition

        // 3. Gestao ativa da posicao aberta (Stop Loss, Trailing Stop 2 estagios, Take Profit)
        if (activePos != null) {
            var updatedPos = activePos
            val trailingTrigger = activePos.entryPrice + max(1.4 * atr, activePos.entryPrice * p.trailingTriggerPct)

            // Estagio 1: protege capital no breakeven + taxas
            if (!updatedPos.trailingActive && livePrice >= trailingTrigger) {
                val breakevenSl = activePos.entryPrice * 1.0028
                updatedPos = updatedPos.copy(
                    stopLoss = max(updatedPos.stopLoss, breakevenSl),
                    trailingActive = true
                )
            }

            // Estagio 2: acompanha alta travando lucro via ATR
            if (updatedPos.trailingActive && atr > 0.0) {
                val dynamicSl = livePrice - (1.25 * atr)
                if (dynamicSl > updatedPos.stopLoss) {
                    updatedPos = updatedPos.copy(stopLoss = dynamicSl)
                }
            }

            val exitReason = when {
                livePrice <= updatedPos.stopLoss -> {
                    if (updatedPos.trailingActive) "TRAILING STOP" else "STOP LOSS"
                }
                livePrice >= updatedPos.takeProfit -> "TAKE PROFIT"
                ema9 < ema21 && macd.histogram < 0.0 && rsi > 68.0 && livePrice > updatedPos.entryPrice * 1.005 -> {
                    "REVERSAO TECNICA"
                }
                else -> null
            }

            if (exitReason != null) {
                val closed = closePosition(state.copy(openPosition = updatedPos), livePrice, exitReason, nowMillis)
                state = closed.first
                val trade = closed.second
                val sign = if (trade.netPnl >= 0.0) "+" else ""
                tradeAlert = "VENDA ($exitReason) BTC @ $${fmt(livePrice)} | Liquido: $sign$${fmt(trade.netPnl)} ($sign${fmt(trade.pnlPercent)}%)"
            } else {
                state = state.copy(
                    openPosition = updatedPos,
                    statusMessage = if (updatedPos.trailingActive) {
                        "Lucro protegido (Trailing Stop ativo)"
                    } else {
                        "Operacao aberta • ${updatedPos.setupName}"
                    }
                )
            }
        } else if (state.isBotRunning) {
            // 4. Sem posicao aberta: verifica trava diaria de perda (Circuit Breaker)
            val maxLossUsdt = -(state.initialDailyBalance * (state.settings.dailyMaxLossPercent / 100.0))
            val realizedToday = state.todayRealizedPnl()

            if (realizedToday <= maxLossUsdt) {
                state = state.copy(
                    statusMessage = "Circuit Breaker (-${fmt1(state.settings.dailyMaxLossPercent)}%) ativo ate 21h"
                )
            } else if (state.availableUsdt >= 10.0) {
                val isBullishCandle = closedCandle.close > closedCandle.open
                val macdImproving = macd.histogram >= macd.prevHistogram

                // SETUP A: Tendencia EMA + MACD + Volume (Murphy + Appel + Wilder)
                val trendSetup = livePrice > ema50 &&
                    ema9 > ema21 &&
                    rsi in 40.0..66.0 &&
                    macdImproving &&
                    volRatio >= 1.10 &&
                    isBullishCandle

                // SETUP B: Reversao na Banda Inferior de Bollinger + RSI (Bollinger + Nison)
                val reversalSetup = prevCandle.close <= bb.lower &&
                    closedCandle.close > bb.lower &&
                    rsi < 38.0 &&
                    rsi > prevRsi &&
                    isBullishCandle

                // SETUP C: Rompimento com Volume Forte (Breakout Momentum)
                val breakoutSetup = ema9 > ema21 &&
                    ema21 > ema50 &&
                    closedCandle.close > prevHigh10 &&
                    volRatio >= 1.45 &&
                    rsi in 50.0..68.0 &&
                    macd.histogram > 0.0

                val chosenSetup = when {
                    trendSetup -> "Tendencia EMA + MACD"
                    breakoutSetup -> "Rompimento + Volume"
                    reversalSetup -> "Reversao Bollinger + RSI"
                    else -> null
                }

                if (chosenSetup != null) {
                    val capitalToUse = state.availableUsdt
                    val entryFee = capitalToUse * SPOT_FEE_RATE
                    val netCapital = capitalToUse - entryFee
                    val btcQty = netCapital / livePrice

                    val riskDist = max(p.atrStopMult * atr, livePrice * p.minRiskPct)
                    val rewardDist = max(p.atrTargetMult * atr, livePrice * p.minRewardPct)

                    val newPos = OpenPosition(
                        entryPrice = livePrice,
                        btcQty = btcQty,
                        investedUsdt = capitalToUse,
                        entryFeeUsdt = entryFee,
                        stopLoss = livePrice - riskDist,
                        takeProfit = livePrice + rewardDist,
                        trailingActive = false,
                        setupName = chosenSetup,
                        profileLabel = state.settings.profile.shortBadge,
                        entryTime = nowMillis
                    )

                    state = state.copy(
                        availableUsdt = 0.0,
                        openPosition = newPos,
                        statusMessage = "COMPRA executada • $chosenSetup"
                    )
                    tradeAlert = "COMPRA BTC @ $${fmt(livePrice)} | $chosenSetup | SL $${fmt0(newPos.stopLoss)} | TP $${fmt0(newPos.takeProfit)}"
                } else {
                    val bias = if (livePrice > ema50) "Vies Alta" else "Vies Baixa"
                    state = state.copy(
                        statusMessage = "Monitorando ${state.settings.profile.shortBadge} ($bias | RSI ${fmt1(rsi)})"
                    )
                }
            }
        } else {
            state = state.copy(statusMessage = "Bot pausado • Clique em INICIAR BOT")
        }

        val signalLabel = when {
            state.openPosition != null -> "COMPRADO • ${state.openPosition!!.setupName}"
            livePrice > ema50 && ema9 > ema21 && macd.histogram >= 0.0 -> "TENDENCIA DE ALTA • PRONTO P/ GATILHO"
            rsi < 36.0 -> "SOBREVENDIDO • RADAR DE REVERSAO"
            livePrice < ema50 -> "FILTRO MACRO BAIXISTA • PROTEGENDO CAIXA"
            else -> "MERCADO LATERAL • FILTRANDO RUIDO"
        }

        val snapshot = IndicatorSnapshot(
            price = livePrice,
            ema9 = ema9,
            ema21 = ema21,
            ema50 = ema50,
            rsi = rsi,
            prevRsi = prevRsi,
            macdLine = macd.macdLine,
            macdSignal = macd.signalLine,
            macdHist = macd.histogram,
            prevMacdHist = macd.prevHistogram,
            bbUpper = bb.upper,
            bbMiddle = bb.middle,
            bbLower = bb.lower,
            atr = atr,
            volumeRatio = volRatio,
            signalText = signalLabel
        )

        return EngineResult(
            newState = state.copy(lastIndicators = snapshot),
            tradeNotification = tradeAlert
        )
    }

    fun closePosition(
        state: SimulationState,
        exitPrice: Double,
        reason: String,
        nowMillis: Long = System.currentTimeMillis()
    ): Pair<SimulationState, CompletedTrade> {
        val pos = state.openPosition ?: throw IllegalStateException("Nenhuma posicao aberta")
        val grossExitUsdt = pos.btcQty * exitPrice
        val exitFee = grossExitUsdt * SPOT_FEE_RATE
        val netExitUsdt = grossExitUsdt - exitFee
        val totalFees = pos.entryFeeUsdt + exitFee
        val netPnl = netExitUsdt - pos.investedUsdt
        val grossPnl = netPnl + totalFees
        val pnlPct = if (pos.investedUsdt > 0.0) (netPnl / pos.investedUsdt) * 100.0 else 0.0

        val completed = CompletedTrade(
            id = UUID.randomUUID().toString(),
            setupName = pos.setupName,
            entryPrice = pos.entryPrice,
            exitPrice = exitPrice,
            btcQty = pos.btcQty,
            grossPnl = grossPnl,
            totalFees = totalFees,
            netPnl = netPnl,
            pnlPercent = pnlPct,
            exitReason = reason,
            entryTime = pos.entryTime,
            exitTime = nowMillis
        )

        val sign = if (netPnl >= 0.0) "+" else ""
        val updatedState = state.copy(
            availableUsdt = state.availableUsdt + netExitUsdt,
            openPosition = null,
            todayTrades = listOf(completed) + state.todayTrades,
            statusMessage = "Saida ($reason): $sign$${fmt(netPnl)}",
            lastUpdated = nowMillis
        )
        return Pair(updatedState, completed)
    }

    fun generateDailyReport(
        state: SimulationState,
        nowMillis: Long = System.currentTimeMillis(),
        resetForNextDay: Boolean = true
    ): EngineResult {
        var workingState = state
        if (workingState.openPosition != null && workingState.lastPrice > 0.0) {
            workingState = closePosition(
                workingState,
                workingState.lastPrice,
                "FECHAMENTO 21H",
                nowMillis
            ).first
        }

        val trades = workingState.todayTrades
        val totalGains = trades.filter { it.netPnl > 0.0 }.sumOf { it.netPnl }
        val totalLosses = trades.filter { it.netPnl < 0.0 }.sumOf { it.netPnl }
        val totalFees = trades.sumOf { it.totalFees }
        val finalBalance = workingState.availableUsdt
        val netPnl = finalBalance - workingState.initialDailyBalance
        val netPnlPercent = if (workingState.initialDailyBalance > 0.0) {
            (netPnl / workingState.initialDailyBalance) * 100.0
        } else {
            0.0
        }

        val report = DailyReport(
            date = formatDateBr(nowMillis),
            initialBalance = workingState.initialDailyBalance,
            finalBalance = finalBalance,
            totalGains = totalGains,
            totalLosses = totalLosses,
            totalFees = totalFees,
            netPnl = netPnl,
            netPnlPercent = netPnlPercent,
            totalTrades = trades.size,
            winningTrades = trades.count { it.netPnl > 0.0 },
            losingTrades = trades.count { it.netPnl < 0.0 },
            bestTradePnl = trades.maxOfOrNull { it.netPnl } ?: 0.0,
            worstTradePnl = trades.minOfOrNull { it.netPnl } ?: 0.0,
            generatedAt = nowMillis
        )

        val todayKey = formatDateKey(nowMillis)
        val updatedReports = listOf(report) + workingState.dailyReports.take(89)
        val nextCapital = if (workingState.settings.resetDailyCapital) {
            INITIAL_DAILY_CAPITAL
        } else {
            finalBalance.coerceAtLeast(10.0)
        }

        val nextState = if (resetForNextDay) {
            workingState.copy(
                initialDailyBalance = nextCapital,
                availableUsdt = nextCapital,
                openPosition = null,
                todayTrades = emptyList(),
                dailyReports = updatedReports,
                lastReportDate = todayKey,
                lastUpdated = nowMillis,
                statusMessage = if (workingState.settings.resetDailyCapital) {
                    "Relatorio 21h salvo! Caixa renovado em $100.00"
                } else {
                    "Relatorio 21h salvo! Novo caixa: $${fmt(nextCapital)}"
                }
            )
        } else {
            workingState.copy(
                dailyReports = updatedReports,
                lastUpdated = nowMillis
            )
        }

        return EngineResult(newState = nextState, generatedReport = report)
    }

    fun formatDateKey(millis: Long): String =
        SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date(millis))

    fun formatDateBr(millis: Long): String =
        SimpleDateFormat("dd/MM/yyyy", Locale("pt", "BR")).format(Date(millis))

    private fun fmt(v: Double): String = String.format(Locale.US, "%.2f", v)
    private fun fmt1(v: Double): String = String.format(Locale.US, "%.1f", v)
    private fun fmt0(v: Double): String = String.format(Locale.US, "%.0f", v)
}
''',

    "app/src/main/java/com/btcsim/trader/data/MarketApiClient.kt": r'''package com.btcsim.trader.data

import com.btcsim.trader.model.Candle
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

object MarketApiClient {

    data class Ticker24h(
        val lastPrice: Double,
        val priceChangePercent: Double,
        val highPrice: Double,
        val lowPrice: Double
    )

    private val baseUrls = listOf(
        "https://data-api.binance.vision",
        "https://api.binance.com",
        "https://api1.binance.com"
    )

    private val client = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(10, TimeUnit.SECONDS)
        .build()

    private fun fetchStringWithFallback(pathAndQuery: String): String {
        var lastError: Exception? = null
        for (base in baseUrls) {
            try {
                val req = Request.Builder()
                    .url("$base$pathAndQuery")
                    .header("User-Agent", "BTCTraderSim/1.0")
                    .build()
                client.newCall(req).execute().use { resp ->
                    if (resp.isSuccessful) {
                        val body = resp.body?.string()
                        if (!body.isNullOrBlank()) return body
                    } else {
                        lastError = Exception("HTTP ${resp.code} em $base")
                    }
                }
            } catch (e: Exception) {
                lastError = e
            }
        }
        throw lastError ?: Exception("Falha de conexao com servidor Binance")
    }

    suspend fun fetchKlines(
        symbol: String = "BTCUSDT",
        interval: String = "5m",
        limit: Int = 120
    ): List<Candle> = withContext(Dispatchers.IO) {
        val body = fetchStringWithFallback("/api/v3/klines?symbol=$symbol&interval=$interval&limit=$limit")
        val array = JSONArray(body)
        val candles = ArrayList<Candle>(array.length())
        for (i in 0 until array.length()) {
            val item = array.getJSONArray(i)
            candles.add(
                Candle(
                    openTime = item.getLong(0),
                    open = item.getString(1).toDouble(),
                    high = item.getString(2).toDouble(),
                    low = item.getString(3).toDouble(),
                    close = item.getString(4).toDouble(),
                    volume = item.getString(5).toDouble()
                )
            )
        }
        candles
    }

    suspend fun fetch24hTicker(symbol: String = "BTCUSDT"): Ticker24h =
        withContext(Dispatchers.IO) {
            val body = fetchStringWithFallback("/api/v3/ticker/24hr?symbol=$symbol")
            val json = JSONObject(body)
            Ticker24h(
                lastPrice = json.getString("lastPrice").toDouble(),
                priceChangePercent = json.getString("priceChangePercent").toDouble(),
                highPrice = json.optString("highPrice", "0").toDoubleOrNull() ?: 0.0,
                lowPrice = json.optString("lowPrice", "0").toDoubleOrNull() ?: 0.0
            )
        }
}
''',

    "app/src/main/java/com/btcsim/trader/data/TradeStorage.kt": r'''package com.btcsim.trader.data

import android.content.Context
import com.btcsim.trader.model.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import org.json.JSONArray
import org.json.JSONObject

object TradeStorage {

    private const val PREFS_NAME = "btc_trader_sim_final_prefs"
    private const val KEY_STATE = "simulation_state_v1"

    private val _stateFlow = MutableStateFlow(SimulationState())
    val stateFlow: StateFlow<SimulationState> = _stateFlow.asStateFlow()

    @Volatile
    private var loaded = false

    @Synchronized
    fun load(context: Context): SimulationState {
        if (loaded) return _stateFlow.value
        val prefs = context.applicationContext.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val raw = prefs.getString(KEY_STATE, null)
        val parsed = if (raw != null) {
            runCatching { deserialize(raw) }.getOrDefault(SimulationState())
        } else {
            SimulationState()
        }
        _stateFlow.value = parsed
        loaded = true
        return parsed
    }

    @Synchronized
    fun save(context: Context, state: SimulationState) {
        _stateFlow.value = state
        loaded = true
        val prefs = context.applicationContext.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putString(KEY_STATE, serialize(state)).apply()
    }

    @Synchronized
    fun updateSettings(context: Context, updater: (BotSettings) -> BotSettings): SimulationState {
        val curr = load(context)
        val updated = curr.copy(settings = updater(curr.settings))
        save(context, updated)
        return updated
    }

    @Synchronized
    fun resetSimulator(context: Context): SimulationState {
        val curr = load(context)
        val fresh = SimulationState(
            isBotRunning = false,
            settings = curr.settings,
            initialDailyBalance = 100.0,
            availableUsdt = 100.0,
            lastPrice = curr.lastPrice,
            priceChange24hPercent = curr.priceChange24hPercent,
            high24h = curr.high24h,
            low24h = curr.low24h,
            recentCandles = curr.recentCandles,
            lastIndicators = curr.lastIndicators,
            statusMessage = "Simulador reiniciado com $100.00"
        )
        save(context, fresh)
        return fresh
    }

    private fun serialize(s: SimulationState): String {
        val root = JSONObject()
        root.put("isBotRunning", s.isBotRunning)
        root.put("initialDailyBalance", s.initialDailyBalance)
        root.put("availableUsdt", s.availableUsdt)
        root.put("lastPrice", s.lastPrice)
        root.put("priceChange24hPercent", s.priceChange24hPercent)
        root.put("high24h", s.high24h)
        root.put("low24h", s.low24h)
        root.put("lastReportDate", s.lastReportDate)
        root.put("lastUpdated", s.lastUpdated)
        root.put("statusMessage", s.statusMessage)

        root.put("settings", JSONObject().apply {
            put("profile", s.settings.profile.id)
            put("resetDailyCapital", s.settings.resetDailyCapital)
            put("dailyMaxLossPercent", s.settings.dailyMaxLossPercent)
            put("soundAlertsEnabled", s.settings.soundAlertsEnabled)
        })

        s.openPosition?.let { pos ->
            root.put("openPosition", JSONObject().apply {
                put("entryPrice", pos.entryPrice)
                put("btcQty", pos.btcQty)
                put("investedUsdt", pos.investedUsdt)
                put("entryFeeUsdt", pos.entryFeeUsdt)
                put("stopLoss", pos.stopLoss)
                put("takeProfit", pos.takeProfit)
                put("trailingActive", pos.trailingActive)
                put("setupName", pos.setupName)
                put("profileLabel", pos.profileLabel)
                put("entryTime", pos.entryTime)
            })
        }

        s.lastIndicators?.let { ind ->
            root.put("lastIndicators", JSONObject().apply {
                put("price", ind.price)
                put("ema9", ind.ema9)
                put("ema21", ind.ema21)
                put("ema50", ind.ema50)
                put("rsi", ind.rsi)
                put("prevRsi", ind.prevRsi)
                put("macdLine", ind.macdLine)
                put("macdSignal", ind.macdSignal)
                put("macdHist", ind.macdHist)
                put("prevMacdHist", ind.prevMacdHist)
                put("bbUpper", ind.bbUpper)
                put("bbMiddle", ind.bbMiddle)
                put("bbLower", ind.bbLower)
                put("atr", ind.atr)
                put("volumeRatio", ind.volumeRatio)
                put("signalText", ind.signalText)
            })
        }

        val tradesArr = JSONArray()
        s.todayTrades.forEach { t ->
            tradesArr.put(JSONObject().apply {
                put("id", t.id)
                put("setupName", t.setupName)
                put("entryPrice", t.entryPrice)
                put("exitPrice", t.exitPrice)
                put("btcQty", t.btcQty)
                put("grossPnl", t.grossPnl)
                put("totalFees", t.totalFees)
                put("netPnl", t.netPnl)
                put("pnlPercent", t.pnlPercent)
                put("exitReason", t.exitReason)
                put("entryTime", t.entryTime)
                put("exitTime", t.exitTime)
            })
        }
        root.put("todayTrades", tradesArr)

        val reportsArr = JSONArray()
        s.dailyReports.forEach { r ->
            reportsArr.put(JSONObject().apply {
                put("date", r.date)
                put("initialBalance", r.initialBalance)
                put("finalBalance", r.finalBalance)
                put("totalGains", r.totalGains)
                put("totalLosses", r.totalLosses)
                put("totalFees", r.totalFees)
                put("netPnl", r.netPnl)
                put("netPnlPercent", r.netPnlPercent)
                put("totalTrades", r.totalTrades)
                put("winningTrades", r.winningTrades)
                put("losingTrades", r.losingTrades)
                put("bestTradePnl", r.bestTradePnl)
                put("worstTradePnl", r.worstTradePnl)
                put("generatedAt", r.generatedAt)
            })
        }
        root.put("dailyReports", reportsArr)

        val candlesArr = JSONArray()
        s.recentCandles.takeLast(60).forEach { c ->
            candlesArr.put(JSONArray().apply {
                put(c.openTime)
                put(c.open)
                put(c.high)
                put(c.low)
                put(c.close)
                put(c.volume)
            })
        }
        root.put("recentCandles", candlesArr)

        return root.toString()
    }

    private fun deserialize(raw: String): SimulationState {
        val root = JSONObject(raw)

        val settingsObj = root.optJSONObject("settings")
        val settings = if (settingsObj != null) {
            BotSettings(
                profile = TradingProfile.fromId(settingsObj.optString("profile", "DAY_5M")),
                resetDailyCapital = settingsObj.optBoolean("resetDailyCapital", true),
                dailyMaxLossPercent = settingsObj.optDouble("dailyMaxLossPercent", 3.0),
                soundAlertsEnabled = settingsObj.optBoolean("soundAlertsEnabled", true)
            )
        } else {
            BotSettings()
        }

        val openPos = root.optJSONObject("openPosition")?.let { p ->
            OpenPosition(
                entryPrice = p.getDouble("entryPrice"),
                btcQty = p.getDouble("btcQty"),
                investedUsdt = p.getDouble("investedUsdt"),
                entryFeeUsdt = p.getDouble("entryFeeUsdt"),
                stopLoss = p.getDouble("stopLoss"),
                takeProfit = p.getDouble("takeProfit"),
                trailingActive = p.optBoolean("trailingActive", false),
                setupName = p.getString("setupName"),
                profileLabel = p.optString("profileLabel", "5M"),
                entryTime = p.getLong("entryTime")
            )
        }

        val indicators = root.optJSONObject("lastIndicators")?.let { ind ->
            IndicatorSnapshot(
                price = ind.optDouble("price", 0.0),
                ema9 = ind.optDouble("ema9", 0.0),
                ema21 = ind.optDouble("ema21", 0.0),
                ema50 = ind.optDouble("ema50", 0.0),
                rsi = ind.optDouble("rsi", 50.0),
                prevRsi = ind.optDouble("prevRsi", 50.0),
                macdLine = ind.optDouble("macdLine", 0.0),
                macdSignal = ind.optDouble("macdSignal", 0.0),
                macdHist = ind.optDouble("macdHist", 0.0),
                prevMacdHist = ind.optDouble("prevMacdHist", 0.0),
                bbUpper = ind.optDouble("bbUpper", 0.0),
                bbMiddle = ind.optDouble("bbMiddle", 0.0),
                bbLower = ind.optDouble("bbLower", 0.0),
                atr = ind.optDouble("atr", 0.0),
                volumeRatio = ind.optDouble("volumeRatio", 1.0),
                signalText = ind.optString("signalText", "")
            )
        }

        val trades = mutableListOf<CompletedTrade>()
        val tArr = root.optJSONArray("todayTrades") ?: JSONArray()
        for (i in 0 until tArr.length()) {
            val o = tArr.getJSONObject(i)
            trades.add(
                CompletedTrade(
                    id = o.getString("id"),
                    setupName = o.getString("setupName"),
                    entryPrice = o.getDouble("entryPrice"),
                    exitPrice = o.getDouble("exitPrice"),
                    btcQty = o.getDouble("btcQty"),
                    grossPnl = o.getDouble("grossPnl"),
                    totalFees = o.getDouble("totalFees"),
                    netPnl = o.getDouble("netPnl"),
                    pnlPercent = o.getDouble("pnlPercent"),
                    exitReason = o.getString("exitReason"),
                    entryTime = o.getLong("entryTime"),
                    exitTime = o.getLong("exitTime")
                )
            )
        }

        val reports = mutableListOf<DailyReport>()
        val rArr = root.optJSONArray("dailyReports") ?: JSONArray()
        for (i in 0 until rArr.length()) {
            val o = rArr.getJSONObject(i)
            reports.add(
                DailyReport(
                    date = o.getString("date"),
                    initialBalance = o.getDouble("initialBalance"),
                    finalBalance = o.getDouble("finalBalance"),
                    totalGains = o.getDouble("totalGains"),
                    totalLosses = o.getDouble("totalLosses"),
                    totalFees = o.getDouble("totalFees"),
                    netPnl = o.getDouble("netPnl"),
                    netPnlPercent = o.getDouble("netPnlPercent"),
                    totalTrades = o.getInt("totalTrades"),
                    winningTrades = o.getInt("winningTrades"),
                    losingTrades = o.getInt("losingTrades"),
                    bestTradePnl = o.optDouble("bestTradePnl", 0.0),
                    worstTradePnl = o.optDouble("worstTradePnl", 0.0),
                    generatedAt = o.getLong("generatedAt")
                )
            )
        }

        val candles = mutableListOf<Candle>()
        val cArr = root.optJSONArray("recentCandles") ?: JSONArray()
        for (i in 0 until cArr.length()) {
            val arr = cArr.getJSONArray(i)
            candles.add(
                Candle(
                    openTime = arr.getLong(0),
                    open = arr.getDouble(1),
                    high = arr.getDouble(2),
                    low = arr.getDouble(3),
                    close = arr.getDouble(4),
                    volume = arr.getDouble(5)
                )
            )
        }

        return SimulationState(
            isBotRunning = root.optBoolean("isBotRunning", false),
            settings = settings,
            initialDailyBalance = root.optDouble("initialDailyBalance", 100.0),
            availableUsdt = root.optDouble("availableUsdt", 100.0),
            openPosition = openPos,
            todayTrades = trades,
            dailyReports = reports,
            recentCandles = candles,
            lastPrice = root.optDouble("lastPrice", 0.0),
            priceChange24hPercent = root.optDouble("priceChange24hPercent", 0.0),
            high24h = root.optDouble("high24h", 0.0),
            low24h = root.optDouble("low24h", 0.0),
            lastIndicators = indicators,
            lastReportDate = root.optString("lastReportDate", ""),
            lastUpdated = root.optLong("lastUpdated", 0L),
            statusMessage = root.optString("statusMessage", "Pronto")
        )
    }
}
''',

    "app/src/main/java/com/btcsim/trader/service/TradingForegroundService.kt": r'''package com.btcsim.trader.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.btcsim.trader.R
import com.btcsim.trader.data.MarketApiClient
import com.btcsim.trader.data.TradeStorage
import com.btcsim.trader.model.DailyReport
import com.btcsim.trader.strategy.TradingEngine
import com.btcsim.trader.ui.MainActivity
import com.btcsim.trader.widget.BtcWidgetProvider
import kotlinx.coroutines.*
import java.util.Locale

class TradingForegroundService : Service() {

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var pollingJob: Job? = null

    companion object {
        const val CHANNEL_BOT = "btc_bot_live"
        const val CHANNEL_ALERTS_SOUND = "btc_bot_alerts_sound"
        const val CHANNEL_ALERTS_SILENT = "btc_bot_alerts_silent"
        const val NOTIF_ID_SERVICE = 1001
        const val NOTIF_ID_REPORT = 2100

        const val ACTION_START = "com.btcsim.trader.START_BOT"

        fun startBot(context: Context) {
            val current = TradeStorage.load(context)
            TradeStorage.save(context, current.copy(isBotRunning = true, statusMessage = "Iniciando motor automatico..."))
            BtcWidgetProvider.updateAllWidgets(context)

            val intent = Intent(context, TradingForegroundService::class.java).apply {
                action = ACTION_START
            }
            runCatching {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    context.startForegroundService(intent)
                } else {
                    context.startService(intent)
                }
            }
        }

        fun stopBot(context: Context) {
            val current = TradeStorage.load(context)
            TradeStorage.save(
                context,
                current.copy(isBotRunning = false, statusMessage = "Bot pausado pelo usuario")
            )
            context.stopService(Intent(context, TradingForegroundService::class.java))
            BtcWidgetProvider.updateAllWidgets(context)
        }

        fun createChannels(context: Context) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                val nm = context.getSystemService(NotificationManager::class.java)
                val botCh = NotificationChannel(
                    CHANNEL_BOT,
                    "Monitoramento ao Vivo BTC/USDT",
                    NotificationManager.IMPORTANCE_LOW
                )
                val soundCh = NotificationChannel(
                    CHANNEL_ALERTS_SOUND,
                    "Trades e Relatorio 21h (Com Som)",
                    NotificationManager.IMPORTANCE_HIGH
                ).apply {
                    enableVibration(true)
                }
                val silentCh = NotificationChannel(
                    CHANNEL_ALERTS_SILENT,
                    "Trades e Relatorio 21h (Silencioso)",
                    NotificationManager.IMPORTANCE_LOW
                )
                nm.createNotificationChannel(botCh)
                nm.createNotificationChannel(soundCh)
                nm.createNotificationChannel(silentCh)
            }
        }

        fun sendTradeNotification(context: Context, message: String, withSound: Boolean) {
            createChannels(context)
            val channelId = if (withSound) CHANNEL_ALERTS_SOUND else CHANNEL_ALERTS_SILENT
            val openIntent = PendingIntent.getActivity(
                context, 10, Intent(context, MainActivity::class.java),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            val notif = NotificationCompat.Builder(context, channelId)
                .setSmallIcon(R.drawable.ic_notif_btc)
                .setContentTitle("Operacao Automatica • BTC/USDT")
                .setContentText(message)
                .setStyle(NotificationCompat.BigTextStyle().bigText(message))
                .setContentIntent(openIntent)
                .setAutoCancel(true)
                .build()

            val nm = context.getSystemService(NotificationManager::class.java)
            nm.notify((System.currentTimeMillis() % 100000).toInt(), notif)
        }

        fun sendReportNotification(context: Context, report: DailyReport, withSound: Boolean) {
            createChannels(context)
            val channelId = if (withSound) CHANNEL_ALERTS_SOUND else CHANNEL_ALERTS_SILENT
            val sign = if (report.netPnl >= 0.0) "+" else ""
            val summary = "Resultado Final: $sign$${fmt(report.netPnl)} ($sign${fmt(report.netPnlPercent)}%)\n" +
                "Total Ganhos: +$${fmt(report.totalGains)} | Perdas: $${fmt(report.totalLosses)}\n" +
                "Trades: ${report.totalTrades} (${report.winningTrades}W / ${report.losingTrades}L) | Taxas: $${fmt(report.totalFees)}\n" +
                "Caixa Final: $${fmt(report.finalBalance)}"

            val openIntent = PendingIntent.getActivity(
                context, 21, Intent(context, MainActivity::class.java),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            val notif = NotificationCompat.Builder(context, channelId)
                .setSmallIcon(R.drawable.ic_notif_btc)
                .setContentTitle("Relatorio Diario 21h — BTC/USDT (${report.date})")
                .setContentText("Resultado: $sign$${fmt(report.netPnl)} ($sign${fmt(report.netPnlPercent)}%)")
                .setStyle(NotificationCompat.BigTextStyle().bigText(summary))
                .setContentIntent(openIntent)
                .setAutoCancel(true)
                .build()

            val nm = context.getSystemService(NotificationManager::class.java)
            nm.notify(NOTIF_ID_REPORT, notif)
        }

        private fun fmt(v: Double): String = String.format(Locale.US, "%.2f", v)
    }

    override fun onCreate() {
        super.onCreate()
        createChannels(this)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val current = TradeStorage.load(this)
        if (!current.isBotRunning) {
            stopSelf()
            return START_NOT_STICKY
        }

        startInForeground("Monitorando BTC/USDT (${current.settings.profile.label})")
        startLoop()
        return START_STICKY
    }

    private fun startInForeground(subtitle: String) {
        val openIntent = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val notification = NotificationCompat.Builder(this, CHANNEL_BOT)
            .setSmallIcon(R.drawable.ic_notif_btc)
            .setContentTitle("BTC Trader Sim • AUTO ON")
            .setContentText(subtitle)
            .setContentIntent(openIntent)
            .setOngoing(true)
            .build()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(
                NOTIF_ID_SERVICE,
                notification,
                ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
            )
        } else {
            startForeground(NOTIF_ID_SERVICE, notification)
        }
    }

    private fun startLoop() {
        pollingJob?.cancel()
        pollingJob = serviceScope.launch {
            while (isActive) {
                runTickOnce()
                delay(15_000L)
            }
        }
    }

    private suspend fun runTickOnce() {
        try {
            val currentState = TradeStorage.load(this)
            if (!currentState.isBotRunning) {
                stopForeground(STOP_FOREGROUND_REMOVE)
                stopSelf()
                return
            }

            val interval = currentState.settings.profile.interval
            val candles = MarketApiClient.fetchKlines("BTCUSDT", interval, 120)
            val ticker = MarketApiClient.fetch24hTicker("BTCUSDT")

            val result = TradingEngine.processMarketTick(
                currentState = currentState,
                candles = candles,
                livePrice = ticker.lastPrice,
                change24hPercent = ticker.priceChangePercent,
                high24h = ticker.highPrice,
                low24h = ticker.lowPrice
            )

            TradeStorage.save(this, result.newState)
            BtcWidgetProvider.updateAllWidgets(this)

            val pnl = result.newState.todayTotalPnl()
            val sign = if (pnl >= 0.0) "+" else ""
            startInForeground(
                "BTC $${fmt(ticker.lastPrice)} (${result.newState.settings.profile.shortBadge}) | Dia: $sign$${fmt(pnl)}"
            )

            val withSound = result.newState.settings.soundAlertsEnabled
            result.tradeNotification?.let { msg ->
                sendTradeNotification(this, msg, withSound)
            }
            result.generatedReport?.let { report ->
                sendReportNotification(this, report, withSound)
            }
        } catch (e: Exception) {
            val st = TradeStorage.load(this)
            TradeStorage.save(this, st.copy(statusMessage = "Reconectando mercado..."))
            BtcWidgetProvider.updateAllWidgets(this)
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        pollingJob?.cancel()
        serviceScope.cancel()
        super.onDestroy()
    }
}
''',

    "app/src/main/java/com/btcsim/trader/service/QuickSyncWorker.kt": r'''package com.btcsim.trader.service

import android.content.Context
import androidx.work.*
import com.btcsim.trader.data.MarketApiClient
import com.btcsim.trader.data.TradeStorage
import com.btcsim.trader.strategy.TradingEngine
import com.btcsim.trader.widget.BtcWidgetProvider

class QuickSyncWorker(
    appContext: Context,
    params: WorkerParameters
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        return try {
            val currentState = TradeStorage.load(applicationContext)
            val interval = currentState.settings.profile.interval
            val candles = MarketApiClient.fetchKlines("BTCUSDT", interval, 120)
            val ticker = MarketApiClient.fetch24hTicker("BTCUSDT")

            val result = TradingEngine.processMarketTick(
                currentState = currentState,
                candles = candles,
                livePrice = ticker.lastPrice,
                change24hPercent = ticker.priceChangePercent,
                high24h = ticker.highPrice,
                low24h = ticker.lowPrice
            )

            TradeStorage.save(applicationContext, result.newState)
            BtcWidgetProvider.updateAllWidgets(applicationContext)

            val withSound = result.newState.settings.soundAlertsEnabled
            result.tradeNotification?.let {
                TradingForegroundService.sendTradeNotification(applicationContext, it, withSound)
            }
            result.generatedReport?.let {
                TradingForegroundService.sendReportNotification(applicationContext, it, withSound)
            }
            Result.success()
        } catch (_: Exception) {
            Result.retry()
        }
    }

    companion object {
        private const val WORK_NAME = "btc_quick_sync_once"

        fun enqueue(context: Context) {
            val req = OneTimeWorkRequestBuilder<QuickSyncWorker>().build()
            WorkManager.getInstance(context).enqueueUniqueWork(
                WORK_NAME,
                ExistingWorkPolicy.REPLACE,
                req
            )
        }
    }
}
''',

    "app/src/main/java/com/btcsim/trader/service/DailyReportWorker.kt": r'''package com.btcsim.trader.service

import android.content.Context
import androidx.work.*
import com.btcsim.trader.data.MarketApiClient
import com.btcsim.trader.data.TradeStorage
import com.btcsim.trader.strategy.TradingEngine
import com.btcsim.trader.widget.BtcWidgetProvider
import java.util.Calendar
import java.util.concurrent.TimeUnit

class DailyReportWorker(
    appContext: Context,
    params: WorkerParameters
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        val state = TradeStorage.load(applicationContext)
        val todayKey = TradingEngine.formatDateKey(System.currentTimeMillis())

        if (state.lastReportDate != todayKey) {
            val livePrice = runCatching {
                MarketApiClient.fetch24hTicker("BTCUSDT").lastPrice
            }.getOrDefault(state.lastPrice)

            val res = TradingEngine.generateDailyReport(
                state = state.copy(lastPrice = livePrice),
                resetForNextDay = true
            )
            TradeStorage.save(applicationContext, res.newState)
            res.generatedReport?.let {
                TradingForegroundService.sendReportNotification(
                    applicationContext,
                    it,
                    res.newState.settings.soundAlertsEnabled
                )
            }
            BtcWidgetProvider.updateAllWidgets(applicationContext)
        }

        scheduleNext21h(applicationContext)
        return Result.success()
    }

    companion object {
        private const val UNIQUE_WORK_NAME = "daily_report_21h_work"

        fun scheduleNext21h(context: Context) {
            val now = Calendar.getInstance()
            val target = Calendar.getInstance().apply {
                set(Calendar.HOUR_OF_DAY, 21)
                set(Calendar.MINUTE, 0)
                set(Calendar.SECOND, 5)
                set(Calendar.MILLISECOND, 0)
                if (!after(now)) {
                    add(Calendar.DAY_OF_YEAR, 1)
                }
            }

            val delayMillis = (target.timeInMillis - now.timeInMillis).coerceAtLeast(10_000L)
            val req = OneTimeWorkRequestBuilder<DailyReportWorker>()
                .setInitialDelay(delayMillis, TimeUnit.MILLISECONDS)
                .build()

            WorkManager.getInstance(context).enqueueUniqueWork(
                UNIQUE_WORK_NAME,
                ExistingWorkPolicy.REPLACE,
                req
            )
        }
    }
}
''',

    "app/src/main/java/com/btcsim/trader/service/BootReceiver.kt": r'''package com.btcsim.trader.service

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.btcsim.trader.widget.BtcWidgetProvider

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            DailyReportWorker.scheduleNext21h(context)
            BtcWidgetProvider.updateAllWidgets(context)
            QuickSyncWorker.enqueue(context)
        }
    }
}
''',

    "app/src/main/java/com/btcsim/trader/widget/BtcWidgetProvider.kt": r'''package com.btcsim.trader.widget

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.widget.RemoteViews
import com.btcsim.trader.R
import com.btcsim.trader.data.TradeStorage
import com.btcsim.trader.service.QuickSyncWorker
import com.btcsim.trader.service.TradingForegroundService
import com.btcsim.trader.ui.MainActivity
import java.util.Locale

class BtcWidgetProvider : AppWidgetProvider() {

    companion object {
        const val ACTION_TOGGLE_BOT = "com.btcsim.trader.ACTION_TOGGLE_BOT"
        const val ACTION_REFRESH = "com.btcsim.trader.ACTION_REFRESH_WIDGET"

        fun updateAllWidgets(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(ComponentName(context, BtcWidgetProvider::class.java))
            if (ids.isNotEmpty()) {
                for (id in ids) {
                    updateSingleWidget(context, manager, id)
                }
            }
        }

        private fun updateSingleWidget(context: Context, manager: AppWidgetManager, widgetId: Int) {
            val state = TradeStorage.load(context)
            val views = RemoteViews(context.packageName, R.layout.widget_btc_trader_5x5)

            views.setTextViewText(R.id.w_profile_badge, state.settings.profile.shortBadge)

            val priceStr = if (state.lastPrice > 0.0) "$${fmt(state.lastPrice)}" else "$ --,--"
            views.setTextViewText(R.id.w_btc_price, priceStr)

            val chg = state.priceChange24hPercent
            val chgSign = if (chg >= 0.0) "+" else ""
            views.setTextViewText(R.id.w_change_24h, "24h: $chgSign${fmt(chg)}%")
            views.setTextColor(
                R.id.w_change_24h,
                Color.parseColor(if (chg >= 0.0) "#0ECB81" else "#F6465D")
            )

            if (state.isBotRunning) {
                views.setTextViewText(R.id.w_bot_badge, "AUTO ON")
                views.setInt(R.id.w_bot_badge, "setBackgroundResource", R.drawable.badge_green)
                views.setTextColor(R.id.w_bot_badge, Color.parseColor("#0ECB81"))
                views.setTextViewText(R.id.w_btn_toggle, "PAUSAR BOT")
            } else {
                views.setTextViewText(R.id.w_bot_badge, "PAUSADO")
                views.setInt(R.id.w_bot_badge, "setBackgroundResource", R.drawable.badge_red)
                views.setTextColor(R.id.w_bot_badge, Color.parseColor("#F6465D"))
                views.setTextViewText(R.id.w_btn_toggle, "INICIAR BOT")
            }

            val equity = state.totalEquity()
            val dailyPnl = state.todayTotalPnl()
            val pnlSign = if (dailyPnl >= 0.0) "+" else ""
            views.setTextViewText(R.id.w_initial_box, "$${fmt(state.initialDailyBalance)}")
            views.setTextViewText(R.id.w_equity, "$${fmt(equity)}")
            views.setTextViewText(
                R.id.w_daily_pnl,
                "$pnlSign$${fmt(dailyPnl)} ($pnlSign${fmt1(state.todayTotalPnlPercent())}%)"
            )
            views.setTextColor(
                R.id.w_daily_pnl,
                Color.parseColor(if (dailyPnl >= 0.0) "#0ECB81" else "#F6465D")
            )

            val pos = state.openPosition
            if (pos != null && state.lastPrice > 0.0) {
                val uPnl = pos.unrealizedPnl(state.lastPrice)
                val uSign = if (uPnl >= 0.0) "+" else ""
                views.setTextViewText(
                    R.id.w_pos_title,
                    "COMPRADO • $uSign$${fmt(uPnl)} (${pos.setupName})"
                )
                views.setTextViewText(
                    R.id.w_pos_details,
                    "Ent: $${fmt0(pos.entryPrice)} | SL: $${fmt0(pos.stopLoss)} | TP: $${fmt0(pos.takeProfit)}"
                )
            } else {
                views.setTextViewText(R.id.w_pos_title, "POSICAO: AGUARDANDO SINAL")
                views.setTextViewText(R.id.w_pos_details, state.statusMessage)
            }

            val ind = state.lastIndicators
            if (ind != null) {
                val emaTrend = if (ind.ema9 > ind.ema21) "ALTA" else "BAIXA"
                val macdTag = if (ind.macdHist >= 0.0) "+" else "-"
                views.setTextViewText(
                    R.id.w_indicators,
                    "EMA: $emaTrend | RSI: ${fmt1(ind.rsi)} | MACD: $macdTag | ATR: $${fmt0(ind.atr)}"
                )
            }

            views.setTextViewText(
                R.id.w_trades_header,
                "TRADES HOJE: ${state.todayTrades.size} • RELATORIO 21H"
            )
            val tradesText = if (state.todayTrades.isEmpty()) {
                val lastRep = state.dailyReports.firstOrNull()
                if (lastRep != null) {
                    val s = if (lastRep.netPnl >= 0.0) "+" else ""
                    "Sem trades encerrados hoje.\nUltimo fechamento (${lastRep.date}): $s$${fmt(lastRep.netPnl)}"
                } else {
                    "Nenhuma operacao encerrada hoje.\nRelatorio automatico agendado para 21:00."
                }
            } else {
                state.todayTrades.take(3).joinToString("\n") { t ->
                    val s = if (t.netPnl >= 0.0) "+" else ""
                    "• ${t.exitReason}: $s$${fmt(t.netPnl)} ($s${fmt1(t.pnlPercent)}%)"
                }
            }
            views.setTextViewText(R.id.w_recent_trades, tradesText)

            val openAppIntent = PendingIntent.getActivity(
                context, 1, Intent(context, MainActivity::class.java),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.widget_header, openAppIntent)

            val toggleIntent = PendingIntent.getBroadcast(
                context, 2,
                Intent(context, BtcWidgetProvider::class.java).setAction(ACTION_TOGGLE_BOT),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.w_btn_toggle, toggleIntent)

            val refreshIntent = PendingIntent.getBroadcast(
                context, 3,
                Intent(context, BtcWidgetProvider::class.java).setAction(ACTION_REFRESH),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.w_btn_refresh, refreshIntent)

            manager.updateAppWidget(widgetId, views)
        }

        private fun fmt(v: Double): String = String.format(Locale.US, "%.2f", v)
        private fun fmt1(v: Double): String = String.format(Locale.US, "%.1f", v)
        private fun fmt0(v: Double): String = String.format(Locale.US, "%.0f", v)
    }

    override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {
        updateAllWidgets(context)
        QuickSyncWorker.enqueue(context)
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        when (intent.action) {
            ACTION_TOGGLE_BOT -> {
                val current = TradeStorage.load(context)
                if (current.isBotRunning) {
                    TradingForegroundService.stopBot(context)
                } else {
                    TradingForegroundService.startBot(context)
                }
            }
            ACTION_REFRESH -> {
                QuickSyncWorker.enqueue(context)
            }
        }
    }
}
''',

    "app/src/main/java/com/btcsim/trader/ui/MainActivity.kt": r'''package com.btcsim.trader.ui

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Assessment
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.ShowChart
import androidx.compose.material.icons.filled.SwapHoriz
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.btcsim.trader.data.TradeStorage
import com.btcsim.trader.model.*
import com.btcsim.trader.service.DailyReportWorker
import com.btcsim.trader.service.QuickSyncWorker
import com.btcsim.trader.service.TradingForegroundService
import com.btcsim.trader.strategy.Indicators
import com.btcsim.trader.strategy.TradingEngine
import com.btcsim.trader.widget.BtcWidgetProvider
import java.text.SimpleDateFormat
import java.util.*

private val BgDark = Color(0xFF0B0E11)
private val CardDark = Color(0xFF181A20)
private val SurfaceDark = Color(0xFF20242C)
private val BorderDark = Color(0xFF2B3139)
private val GreenPro = Color(0xFF0ECB81)
private val RedPro = Color(0xFFF6465D)
private val GoldPro = Color(0xFFFCD535)
private val BluePro = Color(0xFF3898FF)
private val TextMain = Color(0xFFEAECEF)
private val TextSub = Color(0xFF848E9C)

class MainActivity : ComponentActivity() {

    private val requestNotifPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        TradingForegroundService.createChannels(this)
        DailyReportWorker.scheduleNext21h(this)
        TradeStorage.load(this)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
            ) {
                requestNotifPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }

        QuickSyncWorker.enqueue(this)

        setContent {
            val state by TradeStorage.stateFlow.collectAsState()
            TraderAppScreen(
                state = state,
                onToggleBot = {
                    if (state.isBotRunning) {
                        TradingForegroundService.stopBot(this)
                    } else {
                        TradingForegroundService.startBot(this)
                    }
                },
                onSyncNow = { QuickSyncWorker.enqueue(this) },
                onSelectProfile = { profile ->
                    TradeStorage.updateSettings(this) { it.copy(profile = profile) }
                    BtcWidgetProvider.updateAllWidgets(this)
                    QuickSyncWorker.enqueue(this)
                },
                onUpdateSettings = { updater ->
                    TradeStorage.updateSettings(this, updater)
                    BtcWidgetProvider.updateAllWidgets(this)
                },
                onClosePositionManual = {
                    if (state.openPosition != null && state.lastPrice > 0.0) {
                        val closed = TradingEngine.closePosition(state, state.lastPrice, "SAIDA MANUAL").first
                        TradeStorage.save(this, closed)
                        BtcWidgetProvider.updateAllWidgets(this)
                    }
                },
                onGenerateReportNow = {
                    val res = TradingEngine.generateDailyReport(state, resetForNextDay = true)
                    TradeStorage.save(this, res.newState)
                    res.generatedReport?.let {
                        TradingForegroundService.sendReportNotification(
                            this,
                            it,
                            res.newState.settings.soundAlertsEnabled
                        )
                    }
                    BtcWidgetProvider.updateAllWidgets(this)
                },
                onResetSimulator = {
                    TradingForegroundService.stopBot(this)
                    TradeStorage.resetSimulator(this)
                    BtcWidgetProvider.updateAllWidgets(this)
                    QuickSyncWorker.enqueue(this)
                }
            )
        }
    }
}

@Composable
fun TraderAppScreen(
    state: SimulationState,
    onToggleBot: () -> Unit,
    onSyncNow: () -> Unit,
    onSelectProfile: (TradingProfile) -> Unit,
    onUpdateSettings: ((BotSettings) -> BotSettings) -> Unit,
    onClosePositionManual: () -> Unit,
    onGenerateReportNow: () -> Unit,
    onResetSimulator: () -> Unit
) {
    var selectedTab by remember { mutableIntStateOf(0) }

    Scaffold(
        containerColor = BgDark,
        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(CardDark)
                    .statusBarsPadding()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Column {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("BTC/USDT", color = TextMain, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.width(8.dp))
                        Text(
                            state.settings.profile.shortBadge,
                            color = GoldPro,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier
                                .clip(RoundedCornerShape(4.dp))
                                .background(GoldPro.copy(alpha = 0.15f))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                    }
                    Text(
                        "Spot 1x Sem Alavancagem • Caixa $${fmt(state.initialDailyBalance)}",
                        color = TextSub,
                        fontSize = 11.sp
                    )
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onSyncNow) {
                        Icon(Icons.Default.Refresh, contentDescription = "Atualizar", tint = TextMain)
                    }
                    Button(
                        onClick = onToggleBot,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (state.isBotRunning) RedPro else GreenPro
                        ),
                        shape = RoundedCornerShape(8.dp),
                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                    ) {
                        Text(
                            if (state.isBotRunning) "PAUSAR" else "INICIAR",
                            color = Color.White,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        },
        bottomBar = {
            NavigationBar(containerColor = CardDark) {
                val navColors = NavigationBarItemDefaults.colors(
                    selectedIconColor = GoldPro,
                    selectedTextColor = GoldPro,
                    unselectedIconColor = TextSub,
                    unselectedTextColor = TextSub,
                    indicatorColor = BorderDark
                )
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Icon(Icons.Default.ShowChart, contentDescription = null) },
                    label = { Text("Painel", maxLines = 1) },
                    colors = navColors
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Icon(Icons.Default.SwapHoriz, contentDescription = null) },
                    label = { Text("Trades (${state.todayTrades.size})", maxLines = 1) },
                    colors = navColors
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    icon = { Icon(Icons.Default.Assessment, contentDescription = null) },
                    label = { Text("21h", maxLines = 1) },
                    colors = navColors
                )
                NavigationBarItem(
                    selected = selectedTab == 3,
                    onClick = { selectedTab = 3 },
                    icon = { Icon(Icons.Default.Settings, contentDescription = null) },
                    label = { Text("Ajustes", maxLines = 1) },
                    colors = navColors
                )
            }
        }
    ) { padding ->
        Box(modifier = Modifier.padding(padding).fillMaxSize()) {
            when (selectedTab) {
                0 -> DashboardTab(state, onSelectProfile, onClosePositionManual)
                1 -> TradesTab(state)
                2 -> ReportsTab(state.dailyReports, onGenerateReportNow)
                3 -> SettingsTab(state.settings, onUpdateSettings, onSelectProfile, onResetSimulator)
            }
        }
    }
}

@Composable
fun DashboardTab(
    state: SimulationState,
    onSelectProfile: (TradingProfile) -> Unit,
    onCloseManual: () -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Card Cotacao + Grafico Candlestick Pro
        item {
            CardPro {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            if (state.lastPrice > 0.0) "$${fmt(state.lastPrice)}" else "Conectando...",
                            color = Color.White,
                            fontSize = 28.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            state.statusMessage,
                            color = GoldPro,
                            fontSize = 12.sp,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    Column(horizontalAlignment = Alignment.End) {
                        val chg = state.priceChange24hPercent
                        val color = if (chg >= 0.0) GreenPro else RedPro
                        Text(
                            "${if (chg >= 0.0) "+" else ""}${fmt(chg)}%",
                            color = color,
                            fontWeight = FontWeight.Bold,
                            fontSize = 14.sp,
                            modifier = Modifier
                                .clip(RoundedCornerShape(6.dp))
                                .background(color.copy(alpha = 0.15f))
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                        if (state.high24h > 0.0 && state.low24h > 0.0) {
                            Spacer(Modifier.height(4.dp))
                            Text(
                                "Max $${fmt0(state.high24h)} • Min $${fmt0(state.low24h)}",
                                color = TextSub,
                                fontSize = 10.sp
                            )
                        }
                    }
                }

                Spacer(Modifier.height(10.dp))

                // Seletor rapido de Timeframe (Day Trade / Swing Trade)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    TradingProfile.entries.forEach { profile ->
                        val active = state.settings.profile == profile
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(6.dp))
                                .background(if (active) GoldPro.copy(alpha = 0.18f) else SurfaceDark)
                                .border(1.dp, if (active) GoldPro else BorderDark, RoundedCornerShape(6.dp))
                                .clickable { onSelectProfile(profile) }
                                .padding(vertical = 6.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                profile.label,
                                color = if (active) GoldPro else TextSub,
                                fontSize = 11.sp,
                                fontWeight = if (active) FontWeight.Bold else FontWeight.Medium
                            )
                        }
                    }
                }

                Spacer(Modifier.height(10.dp))

                CandlestickChart(
                    candles = state.recentCandles,
                    openPosition = state.openPosition,
                    modifier = Modifier.fillMaxWidth().height(190.dp)
                )

                Spacer(Modifier.height(6.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("EMA 9 (Ouro) • EMA 21 (Azul) • Bandas Bollinger", color = TextSub, fontSize = 10.sp)
                    val timeLabel = if (state.lastUpdated > 0L) {
                        SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date(state.lastUpdated))
                    } else "--:--"
                    Text("Sync: $timeLabel", color = TextSub, fontSize = 10.sp)
                }
            }
        }

        // Card Banca Diaria ($100)
        item {
            val equity = state.totalEquity()
            val pnl = state.todayTotalPnl()
            val pnlPct = state.todayTotalPnlPercent()
            val pnlColor = if (pnl >= 0.0) GreenPro else RedPro

            CardPro {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("GESTAO DE BANCA DIARIA (1x SPOT)", color = TextSub, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Text(
                        if (state.settings.resetDailyCapital) "Reset $100 as 21h" else "Juros Compostos",
                        color = GoldPro,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                }
                Spacer(Modifier.height(10.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    MetricCol("Caixa Inicial", "$${fmt(state.initialDailyBalance)}", TextMain)
                    MetricCol("Patrimonio", "$${fmt(equity)}", Color.White)
                    MetricCol(
                        "Resultado Dia",
                        "${if (pnl >= 0.0) "+" else ""}$${fmt(pnl)} (${fmt1(pnlPct)}%)",
                        pnlColor
                    )
                }
            }
        }

        // Card Posicao Ativa com Barra de Progresso SL -> TP
        state.openPosition?.let { pos ->
            item {
                val uPnl = pos.unrealizedPnl(state.lastPrice)
                val uPct = pos.unrealizedPnlPercent(state.lastPrice)
                val uColor = if (uPnl >= 0.0) GreenPro else RedPro
                val span = (pos.takeProfit - pos.stopLoss).coerceAtLeast(1.0)
                val progress = ((state.lastPrice - pos.stopLoss) / span).toFloat().coerceIn(0f, 1f)

                CardPro {
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(
                            "COMPRADO • ${pos.setupName}",
                            color = GoldPro,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            "${if (uPnl >= 0.0) "+" else ""}$${fmt(uPnl)} (${fmt(uPct)}%)",
                            color = uColor,
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp
                        )
                    }
                    Spacer(Modifier.height(10.dp))
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        MetricCol("Entrada", "$${fmt(pos.entryPrice)}", TextMain)
                        MetricCol(
                            if (pos.trailingActive) "Trailing SL" else "Stop Loss",
                            "$${fmt(pos.stopLoss)}",
                            if (pos.trailingActive) GoldPro else RedPro
                        )
                        MetricCol("Take Profit", "$${fmt(pos.takeProfit)}", GreenPro)
                    }
                    Spacer(Modifier.height(10.dp))
                    LinearProgressIndicator(
                        progress = { progress },
                        modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)),
                        color = if (uPnl >= 0.0) GreenPro else RedPro,
                        trackColor = BorderDark
                    )
                    Spacer(Modifier.height(10.dp))
                    OutlinedButton(
                        onClick = onCloseManual,
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = RedPro)
                    ) {
                        Text("Encerrar Posicao a Mercado Agora")
                    }
                }
            }
        }

        // Card Radar Completo de Indicadores
        item {
            val ind = state.lastIndicators
            CardPro {
                Text(
                    "RADAR TECNICO (${state.settings.profile.label.uppercase()})",
                    color = TextSub,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(Modifier.height(6.dp))
                if (ind != null) {
                    Text(ind.signalText, color = GoldPro, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                    Spacer(Modifier.height(10.dp))
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        MetricCol("EMA 9", "$${fmt0(ind.ema9)}", GoldPro)
                        MetricCol("EMA 21", "$${fmt0(ind.ema21)}", BluePro)
                        MetricCol("EMA 50", "$${fmt0(ind.ema50)}", TextMain)
                    }
                    Spacer(Modifier.height(10.dp))
                    HorizontalDivider(color = BorderDark, thickness = 1.dp)
                    Spacer(Modifier.height(10.dp))
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        MetricCol(
                            "RSI (14)",
                            fmt1(ind.rsi),
                            if (ind.rsi < 36.0) GreenPro else if (ind.rsi > 68.0) RedPro else TextMain
                        )
                        MetricCol(
                            "MACD Hist",
                            "${if (ind.macdHist >= 0.0) "+" else ""}${fmt1(ind.macdHist)}",
                            if (ind.macdHist >= 0.0) GreenPro else RedPro
                        )
                        MetricCol("ATR (14)", "$${fmt0(ind.atr)}", TextMain)
                        MetricCol(
                            "Volume",
                            "${fmt1(ind.volumeRatio)}x",
                            if (ind.volumeRatio >= 1.15) GreenPro else TextSub
                        )
                    }
                } else {
                    Text("Aguardando sincronizacao com a Binance...", color = TextSub, fontSize = 12.sp)
                }
            }
        }
    }
}

@Composable
fun CandlestickChart(
    candles: List<Candle>,
    openPosition: OpenPosition?,
    modifier: Modifier = Modifier
) {
    if (candles.size < 3) {
        Box(
            modifier
                .clip(RoundedCornerShape(8.dp))
                .background(BgDark)
                .border(1.dp, BorderDark, RoundedCornerShape(8.dp)),
            contentAlignment = Alignment.Center
        ) {
            Text("Carregando grafico BTC/USDT...", color = TextSub, fontSize = 12.sp)
        }
        return
    }

    val closes = candles.map { it.close }
    val ema9 = Indicators.calculateEmaSeries(closes, 9)
    val ema21 = Indicators.calculateEmaSeries(closes, 21)
    val (bbUpper, bbLower) = Indicators.calculateBollingerSeries(closes, 20, 2.0)

    Canvas(
        modifier = modifier
            .clip(RoundedCornerShape(8.dp))
            .background(BgDark)
            .border(1.dp, BorderDark, RoundedCornerShape(8.dp))
            .padding(horizontal = 8.dp, vertical = 10.dp)
    ) {
        var minP = minOf(candles.minOf { it.low }, bbLower.minOrNull() ?: Double.MAX_VALUE)
        var maxP = maxOf(candles.maxOf { it.high }, bbUpper.maxOrNull() ?: Double.MIN_VALUE)
        openPosition?.let {
            minP = minOf(minP, it.stopLoss)
            maxP = maxOf(maxP, it.takeProfit)
        }
        val range = (maxP - minP).coerceAtLeast(1.0)
        val stepX = size.width / (candles.size - 1).coerceAtLeast(1)

        fun yFor(price: Double): Float =
            (size.height - ((price - minP) / range) * size.height).toFloat()

        // Grade horizontal discreta
        for (g in 1..3) {
            val gy = size.height * (g / 4f)
            drawLine(BorderDark.copy(alpha = 0.5f), Offset(0f, gy), Offset(size.width, gy), 1f)
        }

        fun drawSeries(series: List<Double>, color: Color, width: Float) {
            if (series.size != candles.size) return
            val path = Path()
            series.forEachIndexed { i, v ->
                val x = i * stepX
                val y = yFor(v)
                if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
            }
            drawPath(path, color = color, style = Stroke(width = width))
        }

        // Bandas de Bollinger
        drawSeries(bbUpper, TextSub.copy(alpha = 0.35f), 1.5f)
        drawSeries(bbLower, TextSub.copy(alpha = 0.35f), 1.5f)

        // Candlesticks
        val bodyWidth = (stepX * 0.62f).coerceIn(2.5f, 9f)
        candles.forEachIndexed { idx, c ->
            val x = idx * stepX
            val color = if (c.close >= c.open) GreenPro else RedPro
            drawLine(color, Offset(x, yFor(c.high)), Offset(x, yFor(c.low)), strokeWidth = 1.6f)
            val openY = yFor(c.open)
            val closeY = yFor(c.close)
            val adjCloseY = if (kotlin.math.abs(closeY - openY) < 1.5f) openY + 1.5f else closeY
            drawLine(color, Offset(x, openY), Offset(x, adjCloseY), strokeWidth = bodyWidth, cap = StrokeCap.Butt)
        }

        // Medias Moveis EMA 9 e EMA 21
        drawSeries(ema9, GoldPro, 2.2f)
        drawSeries(ema21, BluePro, 2.2f)

        // Linhas tracejadas da posicao ativa
        openPosition?.let { pos ->
            val dash = PathEffect.dashPathEffect(floatArrayOf(10f, 8f), 0f)
            drawLine(GoldPro, Offset(0f, yFor(pos.entryPrice)), Offset(size.width, yFor(pos.entryPrice)), 2f, pathEffect = dash)
            drawLine(RedPro, Offset(0f, yFor(pos.stopLoss)), Offset(size.width, yFor(pos.stopLoss)), 2f, pathEffect = dash)
            drawLine(GreenPro, Offset(0f, yFor(pos.takeProfit)), Offset(size.width, yFor(pos.takeProfit)), 2f, pathEffect = dash)
        }
    }
}

@Composable
fun TradesTab(state: SimulationState) {
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        item {
            CardPro {
                Text("RESUMO PARCIAL DO DIA (ATE 21H)", color = TextSub, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    MetricCol("Ganhos", "+$${fmt(state.todayGains())}", GreenPro)
                    MetricCol("Perdas", "$${fmt(state.todayLosses())}", RedPro)
                    MetricCol("Taxas", "$${fmt(state.todayFees())}", TextSub)
                }
            }
        }

        if (state.todayTrades.isEmpty()) {
            item {
                Box(Modifier.fillMaxWidth().padding(top = 48.dp), contentAlignment = Alignment.Center) {
                    Text("Nenhuma operacao finalizada hoje.", color = TextSub)
                }
            }
        } else {
            items(state.todayTrades) { t ->
                val color = if (t.netPnl >= 0.0) GreenPro else RedPro
                val sign = if (t.netPnl >= 0.0) "+" else ""
                CardPro {
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(
                            "${t.exitReason} • ${t.setupName}",
                            color = TextMain,
                            fontWeight = FontWeight.Bold,
                            fontSize = 12.sp,
                            modifier = Modifier.weight(1f)
                        )
                        Text(
                            "$sign$${fmt(t.netPnl)} ($sign${fmt1(t.pnlPercent)}%)",
                            color = color,
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp
                        )
                    }
                    Spacer(Modifier.height(6.dp))
                    Text(
                        "Compra: $${fmt(t.entryPrice)}  ->  Venda: $${fmt(t.exitPrice)} | Taxas: $${fmt(t.totalFees)}",
                        color = TextSub,
                        fontSize = 11.sp
                    )
                    val hhmm = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
                    Text(
                        "${hhmm.format(Date(t.entryTime))} ate ${hhmm.format(Date(t.exitTime))}",
                        color = TextSub,
                        fontSize = 10.sp
                    )
                }
            }
        }
    }
}

@Composable
fun ReportsTab(reports: List<DailyReport>, onForceGenerate: () -> Unit) {
    val totalNet = reports.sumOf { it.netPnl }
    val totalTradesAll = reports.sumOf { it.totalTrades }
    val totalWinsAll = reports.sumOf { it.winningTrades }
    val avgWinRate = if (totalTradesAll > 0) (totalWinsAll * 100.0 / totalTradesAll) else 0.0

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            CardPro {
                Text("FECHAMENTO AUTOMATICO DIARIO AS 21:00", color = GoldPro, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                Spacer(Modifier.height(4.dp))
                Text(
                    "As 21h o simulador encerra eventuais posicoes abertas, apura ganhos, perdas e taxas, dispara notificacao e inicia novo caixa no dia seguinte.",
                    color = TextSub,
                    fontSize = 12.sp
                )
                if (reports.isNotEmpty()) {
                    Spacer(Modifier.height(10.dp))
                    HorizontalDivider(color = BorderDark, thickness = 1.dp)
                    Spacer(Modifier.height(10.dp))
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        MetricCol("Dias", "${reports.size}", TextMain)
                        MetricCol(
                            "Acumulado",
                            "${if (totalNet >= 0.0) "+" else ""}$${fmt(totalNet)}",
                            if (totalNet >= 0.0) GreenPro else RedPro
                        )
                        MetricCol("Acerto Geral", "${fmt1(avgWinRate)}%", GoldPro)
                    }
                }
                Spacer(Modifier.height(12.dp))
                Button(
                    onClick = onForceGenerate,
                    colors = ButtonDefaults.buttonColors(containerColor = GoldPro),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Fechar Dia e Gerar Relatorio Agora", color = BgDark, fontWeight = FontWeight.Bold)
                }
            }
        }

        if (reports.isEmpty()) {
            item {
                Box(Modifier.fillMaxWidth().padding(top = 32.dp), contentAlignment = Alignment.Center) {
                    Text("Nenhum relatorio diario gerado ainda.", color = TextSub)
                }
            }
        } else {
            items(reports) { r ->
                val color = if (r.netPnl >= 0.0) GreenPro else RedPro
                val sign = if (r.netPnl >= 0.0) "+" else ""
                val winRate = if (r.totalTrades > 0) (r.winningTrades * 100.0 / r.totalTrades) else 0.0
                CardPro {
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("Relatorio ${r.date} • 21h", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                        Text("$sign$${fmt(r.netPnl)} ($sign${fmt1(r.netPnlPercent)}%)", color = color, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    }
                    Spacer(Modifier.height(8.dp))
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        MetricCol("Ganhos", "+$${fmt(r.totalGains)}", GreenPro)
                        MetricCol("Perdas", "$${fmt(r.totalLosses)}", RedPro)
                        MetricCol("Taxas", "$${fmt(r.totalFees)}", TextSub)
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(
                        "Caixa Inicial: $${fmt(r.initialBalance)}  ->  Final: $${fmt(r.finalBalance)}",
                        color = TextMain,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                    Text(
                        "Trades: ${r.totalTrades} (${r.winningTrades}W / ${r.losingTrades}L) | Acerto: ${fmt1(winRate)}%",
                        color = TextSub,
                        fontSize = 11.sp
                    )
                }
            }
        }
    }
}

@Composable
fun SettingsTab(
    settings: BotSettings,
    onUpdateSettings: ((BotSettings) -> BotSettings) -> Unit,
    onSelectProfile: (TradingProfile) -> Unit,
    onResetSimulator: () -> Unit
) {
    var showResetDialog by remember { mutableStateOf(false) }

    if (showResetDialog) {
        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            containerColor = CardDark,
            title = { Text("Reiniciar Simulador?", color = Color.White) },
            text = {
                Text(
                    "Isso vai pausar o bot, zerar trades de hoje, limpar relatorios anteriores e voltar o caixa para $100.00.",
                    color = TextSub
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        showResetDialog = false
                        onResetSimulator()
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = RedPro)
                ) {
                    Text("Confirmar Reset", color = Color.White)
                }
            },
            dismissButton = {
                TextButton(onClick = { showResetDialog = false }) {
                    Text("Cancelar", color = TextMain)
                }
            }
        )
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            CardPro {
                Text("PERFIL OPERACIONAL (DAY / SWING TRADE)", color = GoldPro, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                TradingProfile.entries.forEach { profile ->
                    val selected = settings.profile == profile
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                            .clip(RoundedCornerShape(10.dp))
                            .background(if (selected) GoldPro.copy(alpha = 0.12f) else SurfaceDark)
                            .border(1.dp, if (selected) GoldPro else BorderDark, RoundedCornerShape(10.dp))
                            .clickable { onSelectProfile(profile) }
                            .padding(12.dp)
                    ) {
                        Text(
                            profile.label,
                            color = if (selected) GoldPro else TextMain,
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp
                        )
                        Text(profile.description, color = TextSub, fontSize = 11.sp)
                    }
                }
            }
        }

        item {
            CardPro {
                Text("GESTAO DE CAPITAL E RISCO", color = GoldPro, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(10.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f).padding(end = 8.dp)) {
                        Text("Reiniciar caixa em $100 todo dia as 21h", color = TextMain, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                        Text(
                            if (settings.resetDailyCapital) "Ativo: todo dia comeca exatamente com $100.00"
                            else "Desativado: usa Juros Compostos (saldo final vai para o dia seguinte)",
                            color = TextSub,
                            fontSize = 11.sp
                        )
                    }
                    Switch(
                        checked = settings.resetDailyCapital,
                        onCheckedChange = { checked ->
                            onUpdateSettings { it.copy(resetDailyCapital = checked) }
                        }
                    )
                }

                Spacer(Modifier.height(12.dp))
                HorizontalDivider(color = BorderDark, thickness = 1.dp)
                Spacer(Modifier.height(12.dp))

                Text("Trava Diaria de Perda (Circuit Breaker)", color = TextMain, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(8.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf(2.0, 3.0, 5.0).forEach { pct ->
                        val active = settings.dailyMaxLossPercent == pct
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .background(if (active) RedPro.copy(alpha = 0.2f) else SurfaceDark)
                                .border(1.dp, if (active) RedPro else BorderDark, RoundedCornerShape(8.dp))
                                .clickable { onUpdateSettings { it.copy(dailyMaxLossPercent = pct) } }
                                .padding(vertical = 8.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                "-${fmt0(pct)}%",
                                color = if (active) RedPro else TextMain,
                                fontWeight = FontWeight.Bold,
                                fontSize = 13.sp
                            )
                        }
                    }
                }
            }
        }

        item {
            CardPro {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f).padding(end = 8.dp)) {
                        Text("Alertas com Som e Vibracao", color = TextMain, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                        Text("Toca alerta nas compras, vendas e no relatorio das 21h", color = TextSub, fontSize = 11.sp)
                    }
                    Switch(
                        checked = settings.soundAlertsEnabled,
                        onCheckedChange = { checked ->
                            onUpdateSettings { it.copy(soundAlertsEnabled = checked) }
                        }
                    )
                }
            }
        }

        item {
            OutlinedButton(
                onClick = { showResetDialog = true },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.outlinedButtonColors(contentColor = RedPro)
            ) {
                Text("Resetar Todo o Simulador para $100.00")
            }
        }
    }
}

@Composable
fun CardPro(content: @Composable ColumnScope.() -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(14.dp))
            .background(CardDark)
            .border(1.dp, BorderDark, RoundedCornerShape(14.dp))
            .padding(14.dp),
        content = content
    )
}

@Composable
fun MetricCol(label: String, value: String, valueColor: Color) {
    Column {
        Text(label, color = TextSub, fontSize = 10.sp)
        Text(value, color = valueColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
    }
}

private fun fmt(v: Double): String = String.format(Locale.US, "%.2f", v)
private fun fmt1(v: Double): String = String.format(Locale.US, "%.1f", v)
private fun fmt0(v: Double): String = String.format(Locale.US, "%.0f", v)
''',
}


def main():
    created = 0
    for rel_path, content in FILES.items():
        parent = os.path.dirname(rel_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(rel_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        created += 1
        print(f"[OK] {rel_path}")
    print(f"\nProjeto BTCTraderSim gerado com sucesso ({created} arquivos).")


if __name__ == "__main__":
    main()
```

---

<template>
  <nav class="custom-navbar">
    <div class="custom-container">
      <!-- ロゴ -->
      <a class="custom-brand" href="http://127.0.0.1:8000/">FitSpin</a>

      <!-- ナビリンク -->
      <ul class="custom-nav-list">
        <li class="custom-nav-item">
          <router-link class="custom-nav-link" to="/" active-class="active" >ガチャ</router-link>
        </li>
        <li class="custom-nav-item">
          <router-link class="custom-nav-link" to="/calendar">履歴</router-link>
        </li>
      </ul>

      <!-- 右端：ユーザー情報 -->
      <div v-if="user" class="user-info">
        あなた レベル: {{ user.status_level }} ポイント: {{ user.points }}
      </div>
    </div>
  </nav>
</template>

<script setup>
import {ref, onMounted} from 'vue'
const user = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/users/current-user/', {
      credentials: 'include'
    })
    if (!res.ok) throw new Error('APIエラー')
    user.value = await res.json()
  } catch (err) {
    console.error('ユーザー情報取得に失敗:', err)
  }
})
</script>

<style scoped>
.custom-navbar {
  background-color: #5A4DA0; /* 落ち着いたパープル系で #app 背景と統一 */
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  position: relative;
  z-index: 1000;
}

.custom-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap; /* スマホで改行対応 */
  height: 70px;
  padding: 0 20px;
}

/* ロゴ */
.custom-brand {
  font-family: 'Arial Rounded MT Bold','Helvetica Rounded',sans-serif;
  font-weight: bold;
  font-size: 1.6rem;
  color: #fff;
  text-decoration: none;
  margin-right: 30px;
}

/* ナビリンク */
.custom-nav-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 15px;
}

.custom-nav-link {
  color: #fff;
  font-weight: bold;
  text-decoration: none;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
  transition: color 0.3s, text-shadow 0.3s;
}

.custom-nav-link:hover {
  color: #FFD93D; /* ポップ色は控えめに */
  text-shadow: 2px 2px 3px rgba(0,0,0,0.6);
}

/* ユーザー情報右端 */
.user-info {
  margin-left: auto;
  font-size: 0.9rem;
  color: #fff;
  white-space: nowrap;
}

/* ================================
  レスポンシブ対応
=============================== */

/* タブレット 768px以下 */
@media (max-width: 768px) {
  .custom-container {
    height: auto;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  .custom-brand {
    font-size: 1.4rem;
    margin-right: 0;
  }
  .custom-nav-list {
    flex-wrap: wrap;
    gap: 10px;
  }
  .user-info {
    font-size: 0.85rem;
  }
}

/* スマホ 480px以下 */
@media (max-width: 480px) {
  .custom-container {
    padding: 0 12px;
  }
  .custom-brand {
    font-size: 1.2rem;
  }
  .custom-nav-list {
    flex-direction: column;
    width: 100%;
    gap: 6px;
  }
  .custom-nav-link {
    font-size: 0.9rem;
  }
  .user-info {
    font-size: 0.8rem;
  }
}

</style>

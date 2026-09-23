<template>
  <div class="app-wrapper">
    <div class="main-nav-container">
      <div class="main-nav">
        <div class="nav-left">
          <a href="#" :class="{active: activeMainPage==='personal'}" @click.prevent="switchMainPage('personal')">个人</a>
          <a href="#" :class="{active: activeMainPage==='board'}" @click.prevent="switchMainPage('board')">抖音数据榜单</a>
          <a href="#" :class="{active: activeMainPage==='topic'}" @click.prevent="switchMainPage('topic')" class="wide-btn">近期创作话题推荐</a>
        </div>
        <div class="nav-right">
          <button class="login-btn" @click="showLoginModal" v-if="!isLoggedIn">
            <i class="login-icon">🔑</i> 抖音登录
          </button>
          <div class="user-info" v-else>
            <img :src="userInfo.avatar || '/image/default-avatar.png'" alt="用户头像" class="user-avatar">
            <span class="user-name">{{ userInfo.nickname || '用户' }}</span>
            <button class="logout-btn" @click="logout">退出</button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="content-wrapper">
      <!-- 个人页 -->
      <template v-if="activeMainPage==='personal'">
        <div class="container">
          <!-- 个人页内容 -->
          <div class="personal-content">
            <div class="account-analysis">
              <h3>账号数据分析</h3>
              <div class="data-card">
                <div class="data-item">
                  <span class="label">总粉丝数</span>
                  <span class="value">6655.5w</span>
                  <span class="trend up">+3.2%</span>
                </div>
                <div class="data-item">
                  <span class="label">近7天涨粉</span>
                  <span class="value">12.6w</span>
                  <span class="trend up">+8.3%</span>
                </div>
                <div class="data-item">
                  <span class="label">作品数</span>
                  <span class="value">215</span>
                </div>
                <div class="data-item">
                  <span class="label">平均播放</span>
                  <span class="value">36.7w</span>
                  <span class="trend up">+12.4%</span>
                </div>
              </div>
            </div>
            <div class="content-suggestions">
              <h3>内容创作建议</h3>
              <div class="suggestion-list">
                <div class="suggestion-item">
                  <div class="suggestion-title">热门话题</div>
                  <div class="suggestion-content">
                    <span class="tag">#综艺花絮</span>
                    <span class="tag">#明星日常</span>
                    <span class="tag">#幽默搞笑</span>
                  </div>
                </div>
                <div class="suggestion-item">
                  <div class="suggestion-title">最佳发布时间</div>
                  <div class="suggestion-content">
                    <span class="time">18:00-21:00</span>
                    <span class="time">12:30-14:00</span>
                  </div>
                </div>
                <div class="suggestion-item">
                  <div class="suggestion-title">推荐音乐</div>
                  <div class="suggestion-content">
                    <span class="music">《快乐星球》</span>
                    <span class="music">《奔跑吧》</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="fans-analysis">
              <h3>粉丝互动分析</h3>
              <div class="fans-stats">
                <div class="stat-item">
                  <div class="stat-title">粉丝画像</div>
                  <div class="stat-content">
                    <div class="stat-row">
                      <span class="label">性别比例</span>
                      <span class="value">女:男 = 6:4</span>
                    </div>
                    <div class="stat-row">
                      <span class="label">年龄分布</span>
                      <span class="value">18-35岁: 78%</span>
                    </div>
                    <div class="stat-row">
                      <span class="label">地域分布</span>
                      <span class="value">一线城市: 52%</span>
                    </div>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-title">互动率</div>
                  <div class="stat-content">
                    <div class="stat-row">
                      <span class="label">点赞率</span>
                      <span class="value">15.8%</span>
                    </div>
                    <div class="stat-row">
                      <span class="label">评论率</span>
                      <span class="value">4.2%</span>
                    </div>
                    <div class="stat-row">
                      <span class="label">转发率</span>
                      <span class="value">3.5%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- 添加热门视频卡片 -->
          <div class="recent-videos">
            <h3>本人近期热门视频</h3>
            <div class="video-buttons">
              <div class="video-button" @click="openVideo('https://www.douyin.com/user/MS4wLjABAAAAAEtO1dCIZvj4VWbLU4Xce7DgVgsKNMNu88eNR2c2LtY?from_tab_name=main&modal_id=7510457619107613962')">
                <div class="video-title">福建的美食你就吃吧，就没有不好吃</div>
                <div class="video-date">5月31日</div>
                <div class="video-stats">
                  <span class="video-likes"><i class="like-icon">❤️</i> 58.2w</span>
                  <span class="video-comments"><i class="comment-icon">💬</i> 2.1w</span>
                </div>
              </div>
              <div class="video-button" @click="openVideo('https://www.douyin.com/user/MS4wLjABAAAAAEtO1dCIZvj4VWbLU4Xce7DgVgsKNMNu88eNR2c2LtY?from_tab_name=main&modal_id=7511592889311382799')">
                <div class="video-title">一个人做13斤小龙虾...这酸爽...</div>
                <div class="video-date">6月4日</div>
                <div class="video-stats">
                  <span class="video-likes"><i class="like-icon">❤️</i> 42.7w</span>
                  <span class="video-comments"><i class="comment-icon">💬</i> 1.8w</span>
                </div>
              </div>
              <div class="video-button" @click="openVideo('https://www.douyin.com/user/MS4wLjABAAAAAEtO1dCIZvj4VWbLU4Xce7DgVgsKNMNu88eNR2c2LtY?from_tab_name=main&modal_id=7511274713851743514')">
                <div class="video-title">没想到吧还有一条，素材利用率100%的一个局儿</div>
                <div class="video-date">6月3日</div>
                <div class="video-stats">
                  <span class="video-likes"><i class="like-icon">❤️</i> 36.5w</span>
                  <span class="video-comments"><i class="comment-icon">💬</i> 1.5w</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 添加话题匹配度卡片 -->
          <div class="topic-match-card">
            <h3>话题匹配与创作推荐</h3>
            <div class="topic-match-content">
              <div class="match-item">
                <div class="match-video">
                  <div class="match-video-title">福建的美食你就吃吧，就没有不好吃</div>
                  <div class="match-details">
                    <div class="match-topic">
                      <span class="match-label">匹配话题：</span>
                      <span class="match-value">美食探店</span>
                      <span class="match-score high">匹配度：92%</span>
                    </div>
                    <div class="match-suggestion">
                      <span class="suggestion-label">推荐创作方向：</span>
                      <div class="suggestion-tags">
                        <span class="suggestion-tag">地方特色小吃</span>
                        <span class="suggestion-tag">美食制作过程</span>
                        <span class="suggestion-tag">探店攻略</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="match-item">
                <div class="match-video">
                  <div class="match-video-title">一个人做13斤小龙虾...这酸爽...</div>
                  <div class="match-details">
                    <div class="match-topic">
                      <span class="match-label">匹配话题：</span>
                      <span class="match-value">美食制作</span>
                      <span class="match-score high">匹配度：87%</span>
                    </div>
                    <div class="match-suggestion">
                      <span class="suggestion-label">推荐创作方向：</span>
                      <div class="suggestion-tags">
                        <span class="suggestion-tag">大胃王挑战</span>
                        <span class="suggestion-tag">海鲜制作技巧</span>
                        <span class="suggestion-tag">美食vlog</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="match-item">
                <div class="match-video">
                  <div class="match-video-title">没想到吧还有一条，素材利用率100%的一个局儿</div>
                  <div class="match-details">
                    <div class="match-topic">
                      <span class="match-label">匹配话题：</span>
                      <span class="match-value">生活技巧</span>
                      <span class="match-score medium">匹配度：75%</span>
                    </div>
                    <div class="match-suggestion">
                      <span class="suggestion-label">推荐创作方向：</span>
                      <div class="suggestion-tags">
                        <span class="suggestion-tag">生活小窍门</span>
                        <span class="suggestion-tag">创意短视频</span>
                        <span class="suggestion-tag">搞笑日常</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      
      <!-- 抖音数据榜单页 -->
      <template v-if="activeMainPage==='board'">
        <div class="container">
          <div class="main-content board-content">
            <h1>抖音数据榜单</h1>
            <div class="navbar">
              <a href="#" @click.prevent="switchPage('page-daren')" :class="{ active: activePage === 'page-daren' }">达人榜</a>
              <a href="#" @click.prevent="switchPage('page-hot')" :class="{ active: activePage === 'page-hot' }">实时热点</a>
              <a href="#" @click.prevent="switchPage('page-video')" :class="{ active: activePage === 'page-video' }">近期热词</a>
            </div>
            <!-- 达人榜 -->
            <div v-if="activePage === 'page-daren'" id="page-daren">
              <h2>可能感兴趣的达人</h2>
              
              <!-- 加载指示器 -->
              <div v-if="loading.users" class="loading-indicator">
                <div class="spinner"></div>
                <p>加载达人数据中...</p>
              </div>
              
              <!-- 错误提示 -->
              <div v-else-if="error && error.includes('达人数据')" class="error-message">
                <p>{{ error }}</p>
                <button @click="fetchUsers">重试</button>
              </div>
              
              <!-- 达人列表 -->
              <div v-else class="daren-list">
                <div v-for="d in darenData" :key="d.userId || d.name" class="daren-card" @click="openDarenPage(d.url)">
                  <div class="daren-avatar">
                    <img 
                      :src="d.avatar" 
                      :alt="d.name" 
                      @error="handleImageError"
                      class="avatar-image"
                    >
                    <span v-if="d.verified" class="verified-badge" title="已认证">✓</span>
                  </div>
                  <div class="daren-info">
                    <h3 class="daren-name">{{ d.name }}</h3>
                    <p class="daren-category">{{ d.category }}</p>
                    <p class="daren-signature">{{ d.signature || '这个达人很懒，还没有写简介' }}</p>
                    <div class="daren-stats">
                      <div class="stat-item">
                        <span class="stat-label">粉丝数</span>
                        <span class="stat-value">{{ d.fans }}</span>
                      </div>
                      <div class="stat-item">
                        <span class="stat-label">作品数</span>
                        <span class="stat-value">{{ d.videos }}</span>
                      </div>
                      <div class="stat-item">
                        <span class="stat-label">平均点赞</span>
                        <span class="stat-value">{{ d.avgLikes }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="chart-container" ref="darenGraph"></div>
            </div>
            <!-- 实时热点 -->
            <div v-if="activePage === 'page-hot'" id="page-hot" key="hot-page">
              <h2>平台实时热点</h2>
              
              <!-- 加载指示器 -->
              <div v-if="loading.hotWords" class="loading-indicator">
                <div class="spinner"></div>
                <p>加载热点数据中...</p>
              </div>
              
              <!-- 错误提示 -->
              <div v-else-if="error && error.includes('热搜词')" class="error-message">
                <p>{{ error }}</p>
                <button @click="retryHotWords">重试</button>
              </div>
              
              <!-- 热点内容 -->
              <div v-else class="hot-words-flex">
                <!-- 种草热点 -->
                <div class="hot-list-block">
                  <h3><span class="hot-icon">🌱</span> 种草热点</h3>
                  <ul id="hot-list1">
                    <template v-if="hotWordsLeft && hotWordsLeft.length > 0">
                      <li v-for="(word, i) in hotWordsLeft" :key="'left-'+i" :class="['hot-item', { top3: i < 3 }]" @click="openHotLink(word)">
                        <span class="rank">{{ i + 1 }}</span>
                        <span class="title">{{ word.keyword }}</span>
                        <span class="hot-value">{{ word.hot_value }}</span>
                        <span v-if="word.tag" class="hot-tag">{{ word.tag }}</span>
                      </li>
                    </template>
                    <li v-else class="hot-item">
                      <span class="title">暂无数据</span>
                    </li>
                  </ul>
                </div>
                
                <!-- 平台热点 -->
                <div class="hot-list-block">
                  <h3><span class="hot-icon">🔥</span> 平台热点</h3>
                  <ul id="hot-list2">
                    <template v-if="hotWordsRight && hotWordsRight.length > 0">
                      <li v-for="(word, i) in hotWordsRight" :key="'right-'+i" :class="['hot-item', { top3: i < 3 }]" @click="openHotLink(word)">
                        <span class="rank">{{ i + 1 }}</span>
                        <span class="title">{{ word.keyword }}</span>
                        <span class="hot-value">{{ word.hot_value }}</span>
                        <span v-if="word.tag" class="hot-tag">{{ word.tag }}</span>
                      </li>
                    </template>
                    <li v-else class="hot-item">
                      <span class="title">暂无数据</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div v-if="activePage === 'page-video'" id="page-video">
              <h2>近期热词</h2>
              <div class="hot-words-flex">
                <div class="hot-list-block" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 16px;">
                  <h3>近期热词</h3>
                  <div class="word-cloud-container" ref="wordCloudChart" style="display: flex; flex-wrap: wrap; height: auto; min-height: 200px; padding: 20px; justify-content: center;">
                    <div v-for="(word, index) in wordCloudData" :key="index" 
                         style="margin: 10px; padding: 10px 25px; background-color: #f5f5f5; border-radius: 20px; 
                                font-size: 16px; color: #333; display: inline-block; cursor: pointer; min-width: 180px; text-align: center; white-space: nowrap;"
                         :style="{ fontSize: (14 + word.value/10) + 'px', backgroundColor: randomLightColor(index) }">
                      {{ word.name }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      
      <!-- 近期创作话题推荐页 -->
      <template v-if="activeMainPage==='topic'">
        <div class="container">
          <div class="right-sidebar">
            <div class="topic-recommendation">
              <h3>近期创作话题推荐</h3>
              
              <!-- 加载指示器 -->
              <div v-if="loading.hotWords" class="loading-indicator">
                <div class="spinner"></div>
                <p>加载话题数据中...</p>
              </div>
              
              <!-- 错误提示 -->
              <div v-else-if="error && error.includes('热搜词')" class="error-message">
                <p>{{ error }}</p>
                <button @click="retryHotWords">重试</button>
              </div>
              
              <div v-else class="topic-list">
                <div v-for="(topic, index) in topicRecommendations" :key="index" class="topic-item">
                  <span class="topic-rank">{{ index + 1 }}</span>
                  <div class="topic-content">
                    <div class="topic-title">{{ topic.keyword || topic.title }}</div>
                    <div class="topic-stats">
                      <span class="topic-views">{{ topic.hot_value || topic.views }}热度</span>
                      <span v-if="topic.tag" class="topic-tag">{{ topic.tag }}</span>
                    </div>
                  </div>
                  <button class="suggestion-btn" @click.stop="showCreationSuggestion(topic)">
                    创作建议
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 创作建议弹窗 -->
          <div v-if="showSuggestionModal" class="modal-overlay" @click.self="closeSuggestionModal">
            <div class="modal-content">
              <div class="modal-header">
                <h3>创作建议</h3>
                <button class="close-btn" @click="closeSuggestionModal">&times;</button>
              </div>
              <div class="modal-body">
                <h4>{{ currentTopic.keyword || currentTopic.title }}</h4>
                <div class="suggestion-section">
                  <h5>内容方向</h5>
                  <ul>
                    <li v-for="(direction, idx) in getContentDirections(currentTopic)" :key="'dir-'+idx">
                      {{ direction }}
                    </li>
                  </ul>
                </div>
                <div class="suggestion-section">
                  <h5>创作技巧</h5>
                  <ul>
                    <li v-for="(tip, idx) in getCreationTips(currentTopic)" :key="'tip-'+idx">
                      {{ tip }}
                    </li>
                  </ul>
                </div>
                <div class="suggestion-section">
                  <h5>注意事项</h5>
                  <ul>
                    <li v-for="(note, idx) in getNotesToRemember(currentTopic)" :key="'note-'+idx">
                      {{ note }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import api from './utils/api';
import 'echarts-wordcloud';

export default {
  data() {
    return {
      activeMainPage: 'personal',
      activePage: 'page-daren',
      loading: {
        users: false,
        hotWords: false,
        hotVideos: false,
        userVideos: false
      },
      error: null,
      showSuggestionModal: false,
      currentTopic: null,
      isLoggedIn: false,
      userInfo: {
        nickname: '',
        avatar: '',
        userId: ''
      },
      darenData: [
        { 
          name: "陈赫", 
          fans: "6655.5w", 
          videos: "215", 
          avgLikes: "36.7w",
          avatar: "/image/陈赫.png",
          signature: "演员，综艺咖",
          verified: true,
          category: "演员",
          following: "326",
          url: "https://www.douyin.com/user/MS4wLjABAAAAAEtO1dCIZvj4VWbLU4Xce7DgVgsKNMNu88eNR2c2LtY?from_tab_name=main"
        },
        { 
          name: "听泉赏宝", 
          fans: "3687.2w", 
          videos: "782", 
          avgLikes: "17.9w",
          avatar: "/image/听泉赏宝.png",
          signature: "古董收藏爱好者",
          verified: true,
          category: "收藏家",
          following: "8909",
          url: "https://www.douyin.com/user/MS4wLjABAAAAoCCiftUdv439m4Y2Gglyv7ImVZlMSgu_wisIk5zYPJ4?from_tab_name=main"
        },
        { 
          name: "刘德华", 
          fans: "7125.1w", 
          videos: "128", 
          avgLikes: "375.0w",
          avatar: "/image/刘德华.png",
          signature: "演员，歌手",
          verified: true,
          category: "演员",
          following: "0",
          url: "https://www.douyin.com/user/MS4wLjABAAAAU7ibxriLF-GSBF5QKa1Op9hxcMAPVmzmXwXqqvMfrhs?from_tab_name=main"
        },
        { 
          name: "陈翔六点半", 
          fans: "7380.5w", 
          videos: "1024", 
          avgLikes: "110.4w",
          avatar: "/image/陈翔六点半.png",
          signature: "搞笑短剧",
          verified: true,
          category: "搞笑",
          following: "606",
          url: "https://www.douyin.com/user/MS4wLjABAAAA4N4OrZzTSmCPp8vVAqCeyU215Kav2JgFv2Lfy4DNWRs?from_tab_name=main"
        }
      ],
      hotWords: [],
      videoData: [],
      wordCloudData: [
        { name: "520", value: 100 },
        { name: "穿搭", value: 80 },
        { name: "华为", value: 90 },
        { name: "新机", value: 70 },
        { name: "情侣", value: 85 },
        { name: "告白", value: 75 },
        { name: "时尚", value: 65 },
        { name: "科技", value: 60 },
        { name: "生活", value: 55 },
        { name: "美食", value: 50 },
        { name: "旅行", value: 45 },
        { name: "音乐", value: 40 },
        { name: "电影", value: 35 },
        { name: "游戏", value: 30 },
        { name: "运动", value: 25 }
      ],
      chartInstance: null,
      wordCloudInstance: null,
      recommendedTopics: [
        { title: "520告白季", views: "2.3亿", videos: "12.5万" },
        { title: "夏日穿搭指南", views: "1.8亿", videos: "8.9万" },
        { title: "毕业季", views: "1.5亿", videos: "7.2万" },
        { title: "端午美食", views: "1.2亿", videos: "5.6万" },
        { title: "高考加油", views: "1.1亿", videos: "4.8万" },
        { title: "父亲节", views: "9800万", videos: "3.9万" },
        { title: "夏日旅行", views: "8500万", videos: "3.2万" },
        { title: "毕业照", views: "7200万", videos: "2.8万" }
      ],
    };
  },
  computed: {
    sortedDarenData() {
      return [...this.darenData].sort((a, b) => {
        const fansA = parseFloat(a.fans.replace(/,/g, '').replace('w', '0000'));
        const fansB = parseFloat(b.fans.replace(/,/g, '').replace('w', '0000'));
        return fansA - fansB;
      });
    },
    
    // 左侧热点列表（种草热点）
    hotWordsLeft() {
      if (!this.hotWords || this.hotWords.length === 0) return [];
      const mid = Math.floor(this.hotWords.length / 2);
      return this.hotWords.slice(0, mid);
    },
    
    // 右侧热点列表（平台热点）
    hotWordsRight() {
      if (!this.hotWords || this.hotWords.length === 0) return [];
      const mid = Math.floor(this.hotWords.length / 2);
      return this.hotWords.slice(mid);
    },
    
    // 话题推荐列表（基于热搜词）
    topicRecommendations() {
      if (!this.hotWords || this.hotWords.length === 0) {
        return this.recommendedTopics;
      }
      
      // 使用热搜词作为话题推荐
      return this.hotWords.slice(0, 8).map(word => ({
        ...word,
        title: word.keyword,
        views: word.hot_value
      }));
    }
  },
  methods: {
    // 显示创作建议弹窗
    showCreationSuggestion(topic) {
      this.currentTopic = topic;
      this.showSuggestionModal = true;
    },

    // 关闭创作建议弹窗
    closeSuggestionModal() {
      this.showSuggestionModal = false;
    },

    // 获取内容方向建议
    getContentDirections(topic) {
      const keyword = topic.keyword || topic.title;
      const directions = [];
      
      // 根据话题关键词生成内容方向建议
      if (keyword.includes('美食') || keyword.includes('小吃') || keyword.includes('菜')) {
        directions.push('展示特色美食制作过程');
        directions.push('介绍地方特色小吃文化');
        directions.push('分享独特的烹饪技巧和秘方');
      } else if (keyword.includes('旅行') || keyword.includes('景点') || keyword.includes('游')) {
        directions.push('分享旅行目的地的独特风景');
        directions.push('介绍当地特色文化和习俗');
        directions.push('提供实用的旅行攻略和建议');
      } else if (keyword.includes('穿搭') || keyword.includes('时尚') || keyword.includes('搭配')) {
        directions.push('展示日常穿搭技巧和搭配');
        directions.push('分享当季流行趋势解析');
        directions.push('介绍不同场合的着装建议');
      } else if (keyword.includes('运动') || keyword.includes('健身')) {
        directions.push('展示正确的运动姿势和技巧');
        directions.push('分享科学的健身计划和建议');
        directions.push('介绍运动装备的选择和使用');
      } else {
        // 默认建议
        directions.push('从个人经历和感受出发分享故事');
        directions.push('结合当下热点进行创新演绎');
        directions.push('展示独特的视角和见解');
      }
      
      return directions;
    },

    // 获取创作技巧建议
    getCreationTips(topic) {
      const keyword = topic.keyword || topic.title || '';
      const tips = [
        '开场3秒抓住观众注意力，设置悬念或冲突',
        '使用简短文案，突出重点信息',
        '保持视频节奏紧凑，控制时长在1-3分钟',
        '注重画面构图和光线效果',
        '选择适合话题的背景音乐增强氛围'
      ];
      
      // 根据话题关键词添加特定的创作技巧
      if (keyword.includes('美食')) {
        tips.push('使用特写镜头展示食物质感和细节');
        tips.push('加入制作过程中的声音，如食材下锅的声音');
      } else if (keyword.includes('旅行')) {
        tips.push('使用延时摄影展示景点不同时段的美');
        tips.push('结合地图或图文说明介绍地理位置');
      }
      
      return tips;
    },

    // 获取注意事项建议
    getNotesToRemember(topic) {
      const keyword = topic.keyword || topic.title || '';
      const notes = [
        '确保内容真实可信，避免虚假信息',
        '注意保护个人隐私和他人权益',
        '遵守平台规范和相关法律法规',
        '保持内容原创性，避免抄袭',
        '与粉丝保持良性互动，及时回复评论'
      ];
      
      // 根据话题关键词添加特定的注意事项
      if (keyword.includes('美食')) {
        notes.push('标明食材来源和制作难度');
        notes.push('注意食品安全信息的准确性');
      } else if (keyword.includes('旅行')) {
        notes.push('提供准确的景点开放时间和交通信息');
        notes.push('尊重当地文化和习俗');
      }
      
      return notes;
    },

    switchPage(page) {
      // 设置新页面
      this.activePage = page;
      
      // 根据页面类型加载对应数据
      if (page === 'page-daren') {
        if (this.darenData.length === 0) {
          this.fetchUsers();
        }
        // 确保图表初始化
        this.$nextTick(() => {
          this.initChart();
        });
      } else if (page === 'page-hot') {
        // 每次切换到热点页面时，都重新加载热点数据
        this.fetchHotWords();
      } else if (page === 'page-video') {
        if (this.videoData.length === 0) {
          this.fetchHotVideos();
        }
        // 确保词云初始化
        this.$nextTick(() => {
          this.initWordCloud();
        });
      }
    },
    // 生成随机浅色
    randomLightColor(index) {
      const colors = [
        '#e3f2fd', '#e8f5e9', '#f3e5f5', '#fff3e0', '#e0f7fa', 
        '#f1f8e9', '#fff8e1', '#e8eaf6', '#ffebee', '#e0f2f1'
      ];
      return colors[index % colors.length];
    },
    async fetchUsers() {
      this.loading.users = true;
      this.error = null;
      
      // 如果已经有静态数据，就不需要再请求API
      if (this.darenData.length > 0) {
        this.loading.users = false;
        
        // 初始化图表
        this.$nextTick(() => {
          this.initChart();
        });
        return;
      }
      
      try {
        const response = await api.get('/api/users');
        if (response.data && response.data.length > 0) {
          this.darenData = response.data.map(user => ({
            name: user.nickname || '未知用户',
            fans: this.formatNumber(user.fans_count || user.follower_count || 0) + 'w',
            videos: this.formatNumber(user.video_count || 0),
            avgLikes: this.formatNumber(user.likes_count ? Math.floor(user.likes_count / (user.video_count || 1)) : 0) + 'w',
            avatar: user.avatar_url || '',
            signature: user.signature || '',
            verified: user.verified || false,
            category: user.category || '普通用户',
            userId: user.user_id || '',
            url: user.url || ''
          }));
        }
        
        // 初始化图表
        this.$nextTick(() => {
          this.initChart();
        });
      } catch (err) {
        console.error('获取达人数据失败:', err);
        // 错误信息不显示给用户，因为我们已经有静态数据
      } finally {
        this.loading.users = false;
      }
    },

    // 新增方法：获取爬虫爬取的用户数据
    async fetchCrawledUsers() {
      // 如果已经有静态数据，就不需要再请求API
      if (this.darenData.length > 0) {
        return;
      }
      
      try {
        // 尝试从后端获取爬虫爬取的用户数据
        const response = await api.get('/api/crawled-users');
        if (response.data && response.data.length > 0) {
          this.darenData = response.data.map(user => ({
            name: user.nickname || '未知用户',
            fans: this.formatNumber(user.fans_count || user.follower_count || 0) + 'w',
            videos: this.formatNumber(user.video_count || 0),
            avgLikes: this.formatNumber(user.likes_count ? Math.floor(user.likes_count / (user.video_count || 1)) : 0) + 'w',
            avatar: user.avatar_url || '',
            signature: user.signature || '',
            verified: user.verified || false,
            category: user.category || '普通用户',
            userId: user.user_id || '',
            url: user.url || ''
          }));
          console.log('成功获取爬虫数据:', this.darenData.length, '条记录');
        }
      } catch (err) {
        console.error('获取爬虫数据失败:', err);
        // 不需要使用默认数据，因为我们已经有静态数据
      }
    },

    async fetchHotWords() {
      this.loading.hotWords = true;
      this.error = null;
      
      try {
        const response = await api.get('/api/hot-words');
        
        // 直接保存原始数据
        this.hotWords = response.data;
        
        // 更新词云数据
        this.wordCloudData = this.hotWords.map(w => ({
          name: w.keyword,
          value: typeof w.hot_value === 'string' ? 
            parseInt(w.hot_value.replace(/,/g, '')) || Math.random() * 100 : 
            w.hot_value || Math.random() * 100
        }));
        
        console.log('热点数据已加载，共', this.hotWords.length, '条');
      } catch (err) {
        this.error = '获取热搜词失败: ' + err.message;
        console.error('获取热搜词失败:', err);
      } finally {
        this.loading.hotWords = false;
      }
    },

    async fetchHotVideos() {
      this.loading.hotVideos = true;
      try {
        const response = await api.get('/api/hot-videos');
        this.videoData = response.data.map((video, index) => ({
          rank: index + 1,
          title: video.title,
          user: video.author,
          date: this.formatDate(video.create_time),
          likes: this.formatNumber(video.likes) + 'w',
          shares: this.formatNumber(video.shares) + 'w',
          comments: this.formatNumber(video.comments)
        }));
      } catch (err) {
        this.error = '获取热门视频失败: ' + err.message;
        console.error('获取热门视频失败:', err);
      } finally {
        this.loading.hotVideos = false;
      }
    },

    formatNumber(num) {
      if (num >= 10000) {
        return (num / 10000).toFixed(1);
      }
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },

    formatDate(timestamp) {
      const date = new Date(timestamp);
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${month}-${day} ${hours}:${minutes}`;
    },

    initChart() {
      if (this.$refs.darenGraph) {
        // 如果已有图表实例，先销毁
        if (this.chartInstance) {
          this.chartInstance.dispose();
        }
        
        this.chartInstance = echarts.init(this.$refs.darenGraph);
        
        // 处理数据，确保数值正确
        const chartData = this.sortedDarenData.map(d => {
          // 处理粉丝数，移除单位并转为数字
          let fans = d.fans;
          if (typeof fans === 'string') {
            // 处理带有w的数字，例如"6655.5w" => 6655.5
            fans = parseFloat(fans.replace(/,/g, '').replace('w', ''));
          }
          
          // 处理平均点赞数，移除单位并转为数字
          let avgLikes = d.avgLikes;
          if (typeof avgLikes === 'string') {
            avgLikes = parseFloat(avgLikes.replace(/,/g, '').replace('w', ''));
          }
          
          // 处理视频数，移除逗号并转为数字
          let videos = d.videos;
          if (typeof videos === 'string') {
            videos = parseFloat(videos.replace(/,/g, ''));
          }
          
          return {
            name: d.name,
            fans,
            avgLikes,
            videos
          };
        });
        
        const option = {
          title: {
            text: '达人数据分析',
            left: 'center',
            textStyle: {
              color: '#333',
              fontWeight: 'normal',
              fontSize: 18
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
            formatter: function(params) {
              const dataIndex = params[0].dataIndex;
              const data = chartData[dataIndex];
              return `
                <div style="font-weight:bold;margin-bottom:5px;">${data.name}</div>
                <div>
                  <span style="display:inline-block;margin-right:5px;border-radius:50%;width:10px;height:10px;background-color:#ff2c54;"></span>
                  粉丝数: ${data.fans}w
                </div>
                <div>
                  <span style="display:inline-block;margin-right:5px;border-radius:50%;width:10px;height:10px;background-color:#2ecc71;"></span>
                  平均点赞: ${data.avgLikes}w
                </div>
                <div>
                  <span style="display:inline-block;margin-right:5px;border-radius:50%;width:10px;height:10px;background-color:#3498db;"></span>
                  视频数: ${data.videos}
                </div>
              `;
            }
          },
          legend: {
            data: ['粉丝数(万)', '平均点赞(万)', '视频数量'],
            top: 30
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: chartData.map(d => d.name),
            axisLabel: {
              interval: 0,
              rotate: 30,
              margin: 10,
              formatter: function(value) {
                if (value.length > 6) {
                  return value.substring(0, 6) + '...';
                }
                return value;
              }
            }
          },
          yAxis: [
            {
              type: 'value',
              name: '粉丝/点赞数(万)',
              position: 'left',
              axisLabel: {
                formatter: '{value}'
              }
            },
            {
              type: 'value',
              name: '视频数量',
              position: 'right',
              axisLabel: {
                formatter: '{value}'
              }
            }
          ],
          series: [
            {
              name: '粉丝数(万)',
              type: 'bar',
              data: chartData.map(d => d.fans),
              itemStyle: {
                color: '#ff2c54'
              }
            },
            {
              name: '平均点赞(万)',
              type: 'bar',
              data: chartData.map(d => d.avgLikes),
              itemStyle: {
                color: '#2ecc71'
              }
            },
            {
              name: '视频数量',
              type: 'line',
              yAxisIndex: 1,
              data: chartData.map(d => d.videos),
              itemStyle: {
                color: '#3498db'
              }
            }
          ]
        };

        this.chartInstance.setOption(option);
        
        // 添加窗口大小变化监听
        window.addEventListener('resize', this.resizeChart);
      }
    },
    resizeChart() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    },
    initWordCloud() {
      if (this.$refs.wordCloudChart) {
        this.wordCloudInstance = echarts.init(this.$refs.wordCloudChart);
        const option = {
          backgroundColor: 'transparent',
          tooltip: {
            show: true
          },
          series: [{
            type: 'wordCloud',
            shape: 'circle',
            left: 'center',
            top: 'center',
            width: '90%',
            height: '90%',
            right: null,
            bottom: null,
            sizeRange: [12, 60],
            rotationRange: [-90, 90],
            rotationStep: 45,
            gridSize: 8,
            drawOutOfBound: false,
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              color: function () {
                return 'rgb(' + [
                  Math.round(Math.random() * 160 + 95),
                  Math.round(Math.random() * 160 + 95),
                  Math.round(Math.random() * 160 + 95)
                ].join(',') + ')';
              }
            },
            emphasis: {
              textStyle: {
                shadowBlur: 10,
                shadowColor: '#333'
              }
            },
            data: this.wordCloudData
          }]
        };
        this.wordCloudInstance.setOption(option);
      }
    },
    resizeWordCloud() {
      if (this.wordCloudInstance) {
        this.wordCloudInstance.resize();
      }
    },
    retryLoading() {
      this.error = null;
      this.fetchUsers();
      this.fetchHotWords();
      this.fetchHotVideos();
    },
    openHotLink(word) {
      if (word && word.link) {
        window.open(word.link, '_blank');
      }
    },
    switchMainPage(page) {
      this.activeMainPage = page;
      
      // 如果切换到榜单页面，默认显示达人榜并加载数据
      if (page === 'board') {
        this.activePage = 'page-daren';
        
        // 延迟一下再初始化图表，确保DOM已经更新
        this.$nextTick(() => {
          this.initChart();
        });
      }
      
      // 如果切换到话题推荐页面，确保热点数据已加载
      if (page === 'topic' && this.hotWords.length === 0) {
        this.fetchHotWords();
      }
    },
    retryHotWords() {
      this.error = null;
      this.fetchHotWords();
    },
    handleImageError(event) {
      // 使用默认头像替代加载失败的图片
      event.target.src = 'https://p3-pc.douyinpic.com/img/aweme-avatar/tos-cn-avt-0015_a34944dd8e748750a8d5a90b0f7d7d0a~c5_300x300.jpeg?from=2956013662';
    },
    openDarenPage(url) {
      if (url) {
        window.open(url, '_blank');
      }
    },
    // 打开视频链接
    openVideo(url) {
      if (url) {
        window.open(url, '_blank');
      }
    },
    // 显示登录弹窗
    showLoginModal() {
      // 模拟抖音登录
      this.simulateLogin();
    },
    
    // 模拟登录过程
    simulateLogin() {
      // 显示加载状态
      this.loading.login = true;
      
      // 模拟API请求延迟
      setTimeout(() => {
        // 模拟登录成功
        this.isLoggedIn = true;
        this.userInfo = {
          nickname: '抖音用户',
          avatar: '/image/default-avatar.png',
          userId: 'user_' + Math.floor(Math.random() * 1000000)
        };
        
        // 关闭加载状态
        this.loading.login = false;
        
        // 提示登录成功
        alert('登录成功！');
      }, 1000);
    },
    
    // 退出登录
    logout() {
      this.isLoggedIn = false;
      this.userInfo = {
        nickname: '',
        avatar: '',
        userId: ''
      };
    },
  },
  watch: {
    activePage: {
      handler(newVal) {
        if (newVal === 'page-daren') {
          this.$nextTick(() => {
            this.initChart();
            this.resizeChart();
          });
        }
        if (newVal === 'page-video') {
          this.$nextTick(() => {
            this.initWordCloud();
            this.resizeWordCloud();
          });
        }
        if (newVal === 'page-hot') {
          this.$nextTick(() => {
            // 确保热点数据已加载
            if (this.hotWords.length === 0) {
              this.fetchHotWords();
            }
          });
        }
      }
    },
    sortedDarenData: {
      handler(newVal) {
        if (this.chartInstance) {
          const option = {
            xAxis: {
              data: newVal.map(d => d.name)
            },
            series: [
              {
                data: newVal.map(d => parseFloat(d.avgLikes.replace('w', '')))
              },
              {
                data: newVal.map(d => parseFloat(d.videos.replace(',', '')))
              }
            ]
          };
          this.chartInstance.setOption(option);
        }
      },
      deep: true
    }
  },
  mounted() {
    // 添加窗口大小变化监听
    window.addEventListener('resize', this.resizeChart);
    window.addEventListener('resize', this.resizeWordCloud);
    
    // 获取初始数据
    if (this.activeMainPage === 'board') {
      if (this.activePage === 'page-daren') {
        this.fetchUsers();
      } else if (this.activePage === 'page-hot') {
        this.fetchHotWords();
      } else if (this.activePage === 'page-video') {
        this.fetchHotVideos();
      }
    }
    
    this.$nextTick(() => {
      if (this.activeMainPage === 'board') {
        if (this.activePage === 'page-daren') {
          this.initChart();
        } else if (this.activePage === 'page-video') {
          this.initWordCloud();
        }
      }
    });
  },
  beforeUnmount() {
    // 移除事件监听器
    window.removeEventListener('resize', this.resizeChart);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
    if (this.wordCloudInstance) {
      this.wordCloudInstance.dispose();
    }
  }
};
</script>

<style>
body {
    background: #f4f7fa;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #222;
    display: flex;
    justify-content: center;
    min-height: 100vh;
}

.app-wrapper {
  width: 100%;
  max-width: 2800px;
  margin: 0 auto;
  padding: 0 40px;
  box-sizing: border-box;
}

.content-wrapper {
  width: 100%;
  max-width: 2800px;
  margin: 0 auto;
  padding-top: 80px; /* 为固定导航栏留出空间 */
}

.main-nav-container {
  width: 100%;
  display: flex;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  box-sizing: border-box;
  background-color: #f4f7fa;
  padding: 10px 40px;
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 2800px;
  box-sizing: border-box;
}

.container {
  display: flex;
  gap: 20px;
  max-width: 2800px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 0;
  box-sizing: border-box;
}

.main-content {
  width: 100%;
  max-width: 2800px;
  margin: 0 auto;
  padding: 40px;
  box-sizing: border-box;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 10px 50px rgba(0,0,0,0.12), 0 3px 8px rgba(0,0,0,0.06);
}

h1 {
    text-align: center;
    color: #0288d1;
    margin-bottom: 50px;
    font-size: 2.5rem;
    letter-spacing: 2px;
}

h2 {
    color: #333;
    margin-bottom: 30px;
    border-left: 5px solid #0288d1;
    padding-left: 15px;
    font-size: 1.6rem;
    font-weight: 600;
}

h3 {
    color: #0288d1;
    font-size: 1.2rem;
    margin-bottom: 15px;
    font-weight: 500;
}

.section {
    background: #f9fbfd;
    border-radius: 10px;
    padding: 24px;
    margin-bottom: 28px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.navbar {
    display: flex;
    gap: 40px;
    justify-content: center;
    margin-bottom: 45px;
}

.navbar a {
    text-decoration: none;
    color: #333;
    font-weight: bold;
    font-size: 20px;
    padding: 12px 32px;
    border-radius: 10px;
    transition: background 0.2s, color 0.2s;
    background: #f5f5f5;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.navbar a.active, .navbar a:hover {
    background: #0288d1;
    color: #fff;
}

.hidden {
    display: none;
}

/* 统一表格样式 */
.hot-list, .video-table {
  width: 100%;
  font-size: 1.2rem;
  border-collapse: collapse;
  margin-bottom: 30px;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.hot-list th, .hot-list td, .video-table th, .video-table td {
  padding: 18px 20px;
  border: 1px solid #f0f0f0;
  text-align: left;
}

.hot-list th, .video-table th {
    background: #f5f8fa;
    color: #0288d1;
    font-weight: 600;
}

.hot-list tr:nth-child(even), .video-table tr:nth-child(even) {
    background: #f9fbfd;
}

.hot-list tr:hover, .video-table tr:hover {
    background: #e3f2fd;
    transition: background 0.2s;
}

ol {
    padding-left: 22px;
    margin: 0 0 10px 0;
}

ol li {
    margin-bottom: 8px;
    font-size: 1rem;
    line-height: 1.6;
}

.right-sidebar {
    width: 100%;
    max-width: 2800px;
    margin: 0 auto;
    box-sizing: border-box;
}

.topic-recommendation {
    background: #fff;
    border-radius: 24px;
    box-shadow: 0 10px 50px rgba(0,0,0,0.12), 0 3px 8px rgba(0,0,0,0.06);
    padding: 50px;
    width: 100%;
}

.topic-recommendation h3 {
    color: #0288d1;
    font-size: 1.8rem;
    margin-bottom: 40px;
    padding-bottom: 18px;
    border-bottom: 3px solid #f0f0f0;
}

.topic-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.topic-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 25px;
  border-radius: 16px;
  transition: background-color 0.2s;
  background: #f8f9fa;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.topic-item:hover {
  background-color: #f5f8fa;
}

.topic-rank {
    width: 40px;
    height: 40px;
    background: #ff6b6b;
    color: white;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.3rem;
}

.topic-content {
    flex: 1;
}

.topic-title {
    font-weight: 500;
    color: #333;
    margin-bottom: 12px;
    font-size: 1.5rem;
}

.topic-stats {
    display: flex;
    gap: 25px;
    font-size: 1.2rem;
    color: #666;
}

.topic-views, .topic-videos {
    display: flex;
    align-items: center;
    font-weight: 500;
}

.trend-graph {
    width: 100%;
    height: 100%;
    background: none;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #b0bec5;
    font-size: 1.2rem;
    letter-spacing: 1px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* 统一图表容器大小 */
.chart-container {
  width: 100%;
  height: 600px;
  margin-top: 30px;
  background: #f9fbfd;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* 统一热点列表样式 */
#hot-list1, #hot-list2 {
  list-style: none;
  padding: 0;
  margin: 0;
  background: none;
  box-shadow: none;
}

.hot-words-flex {
  display: flex;
  gap: 40px;
  justify-content: space-between;
  align-items: flex-start;
  margin: 0 auto;
  max-width: 100%;
}

.hot-list-block {
  flex: 1;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 3px 12px rgba(0,0,0,0.1);
  padding: 25px 0 20px 0;
  min-width: 450px;
}

.hot-list-block h3 {
  text-align: center;
  font-size: 1.3rem;
  margin-bottom: 20px;
  letter-spacing: 1px;
}

.hot-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 1.15rem;
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-item:hover {
  background: #f5faff;
}

.hot-item.top3 {
  background: linear-gradient(90deg, #fffbe7 0%, #ffe082 100%);
}

.rank {
  width: 28px;
  text-align: right;
  font-weight: bold;
  color: #ff6b6b;
  margin-right: 8px;
  font-size: 1.1em;
}

.title {
  flex: 1;
  color: #222;
  font-weight: 500;
  margin-right: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hot-value {
  min-width: 60px;
  text-align: right;
  color: #ff9800;
  font-weight: bold;
  margin-right: 8px;
  font-size: 1em;
}

.hot-tag {
  background: #e6f7ff;
  color: #0288d1;
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 0.9em;
  margin-left: 8px;
}

@media (max-width: 2100px) {
  .main-content {
    width: calc(100% - 40px);
    max-width: 2100px;
  }
  
  .right-sidebar {
    width: calc(100% - 40px);
    max-width: 2100px;
  }
}

@media (max-width: 1900px) {
  .main-content {
    width: calc(100% - 40px);
    max-width: 1900px;
  }
  
  .right-sidebar {
    width: calc(100% - 40px);
    max-width: 1900px;
  }
}

@media (max-width: 1400px) {
  .main-content {
    width: calc(100% - 40px);
    max-width: 1400px;
    padding: 30px;
  }
  
  .right-sidebar {
    width: calc(100% - 40px);
    max-width: 1400px;
  }
  
  .topic-list {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  }
  
  .topic-recommendation {
    padding: 35px;
  }
  
  .hot-words-section {
    padding: 30px;
  }
  
  .word-cloud-container {
    height: 550px;
  }
  
  .hot-list-block {
    min-width: 350px;
  }
  
  .chart-container, .word-cloud-container {
    height: 500px;
  }
}

@media (max-width: 1600px) {
  .topic-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .topic-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .topic-item {
    padding: 20px;
  }
  
  .topic-title {
    font-size: 1.3rem;
  }
}

@media (max-width: 900px) {
  .topic-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 1000px) {
  .hot-words-flex {
    flex-direction: column;
  }
  
  .hot-list-block {
    width: 100%;
    margin-bottom: 20px;
  }
}

/* 左侧边栏样式 */
.left-sidebar {
  width: 1000px;
  flex-shrink: 0;
  box-sizing: border-box;
}

.personal-content {
  display: flex;
  gap: 40px;
  max-width: 2200px;
  margin: 0 auto;
  justify-content: center;
  align-items: stretch;
  width: 100%;
  padding: 30px 0;
  flex-wrap: wrap;
}

.account-analysis, .content-suggestions, .fans-analysis {
  flex: 1;
  min-width: 300px;
  max-width: 2000px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 32px rgba(0,0,0,0.08), 0 1.5px 4px rgba(0,0,0,0.03);
  padding: 36px 32px 32px 32px;
  font-size: 1.18rem;
  height: auto;
  min-height: 450px;
  width: calc(33.33% - 40px);
  box-sizing: border-box;
  overflow-y: auto;
}

.account-analysis h3, .content-suggestions h3, .fans-analysis h3 {
  font-size: 1.45rem;
  margin-bottom: 22px;
}

.data-item .label, .stat-row .label, .suggestion-title {
  font-size: 1.08rem;
}

.data-item .value, .stat-row .value {
  font-size: 1.32rem;
}

.data-card {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 15px;
}

.data-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.data-item .label {
  color: #666;
  font-size: 0.9rem;
}

.data-item .value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.trend {
  font-size: 0.85rem;
  padding: 2px 6px;
  border-radius: 4px;
}

.trend.up {
  color: #52c41a;
  background: rgba(82, 196, 26, 0.1);
}

.trend.down {
  color: #ff4d4f;
  background: rgba(255, 77, 79, 0.1);
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 15px;
}

.suggestion-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.suggestion-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
}

.suggestion-content {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: #e6f7ff;
  color: #1890ff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.time, .music {
  background: #f6ffed;
  color: #52c41a;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.fans-stats {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 15px;
}

.stat-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.stat-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-row .label {
  color: #666;
  font-size: 0.9rem;
}

.stat-row .value {
  font-weight: 500;
  color: #333;
}

.fans-analysis {
  font-size: 1rem;
}

.fans-analysis h3 {
  font-size: 1.45rem;
}

.fans-analysis .stat-row .label {
  color: #666;
  font-size: 0.9rem;
}

.fans-analysis .stat-row .value {
  font-weight: 500;
  color: #333;
  font-size: 1rem;
}

.fans-analysis .stat-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
  font-size: 1rem;
}

/* 响应式调整 */
@media (max-width: 2800px) {
    .container {
        flex-direction: column;
        width: calc(100% - 40px);
        margin: 40px auto 0;
        padding: 20px;
    }
    
    .left-sidebar, .right-sidebar {
        width: 100%;
    }
    
    .main-content {
        width: 100%;
        max-width: 100%;
    }
}

/* 加载状态样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #0288d1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1.2rem;
  color: #333;
}

/* 错误提示样式 */
.error-message {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #ffebee;
  color: #c62828;
  padding: 15px 25px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 15px;
}

.retry-button {
  background: #0288d1;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 12px;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #0277bd;
}

.hot-words-section {
  margin: 40px 0;
  padding: 40px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  width: 100%;
}

.hot-words-section h3 {
  color: #ff6b00;
  font-size: 1.5rem;
  margin-bottom: 25px;
  font-weight: bold;
  text-align: center;
}

.word-cloud-container {
  width: 100%;
  height: 650px;
  margin-top: 30px;
}

.nav-left {
  display: flex;
  gap: 40px;
  justify-content: center;
  flex: 1;
}

.nav-right {
  display: flex;
  align-items: center;
  min-width: 150px;
  justify-content: flex-end;
}

.main-nav a {
  font-size: 1.2rem;
  color: #0288d1;
  padding: 10px 32px;
  border-radius: 8px;
  background: #f5f5f5;
  font-weight: bold;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
  width: 150px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.main-nav a.active, .main-nav a:hover {
  background: #0288d1;
  color: #fff;
}

.main-nav a.wide-btn {
  width: 220px;
}

.login-btn {
  background: #333;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 150px;
  justify-content: center;
}

.login-btn:hover {
  background: #000;
}

.login-icon {
  font-style: normal;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 150px;
  justify-content: flex-end;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ff2c54;
}

.user-name {
  font-weight: 500;
  color: #333;
}

.logout-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background: #e0e0e0;
}

@media (max-width: 1200px) {
  .personal-content {
    flex-direction: column;
    gap: 20px;
    max-width: 98vw;
    padding: 10px 0;
  }
  
  .account-analysis, .content-suggestions, .fans-analysis {
    width: 100%;
    min-width: auto;
    height: auto;
    margin-bottom: 20px;
  }
  
  .topic-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
  
  .video-button {
    min-width: 100%;
    margin-bottom: 15px;
  }
}

@media (min-width: 1201px) and (max-width: 1600px) {
  .personal-content {
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .account-analysis, .content-suggestions, .fans-analysis {
    width: calc(50% - 20px);
    min-width: 450px;
    margin-bottom: 20px;
  }
}

@media (min-width: 1601px) {
  .account-analysis, .content-suggestions, .fans-analysis {
    min-width: 450px;
  }
}

@media (max-width: 768px) {
  .topic-list {
    display: flex;
    flex-direction: column;
  }
}

/* 加载指示器样式 */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 44, 84, 0.2);
  border-left-color: #ff2c54;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 错误提示样式 */
.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 30px;
  border-radius: 8px;
  margin: 20px 0;
  text-align: center;
}

.error-message button {
  background-color: #ff2c54;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 12px;
  transition: background-color 0.3s;
}

.error-message button:hover {
  background-color: #e6194b;
}

/* 无数据提示样式 */
.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
}

.no-data button {
  background: #0288d1;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
  font-weight: bold;
}

/* 创作建议按钮样式 */
.suggestion-btn {
  background: #0288d1;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
  align-self: center;
}

.suggestion-btn:hover {
  background-color: #0277bd;
}

/* 创作建议弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 16px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #0288d1;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  line-height: 1;
}

.modal-body {
  padding: 25px;
}

.modal-body h4 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 1.3rem;
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.suggestion-section {
  margin-bottom: 25px;
}

.suggestion-section h5 {
  color: #0288d1;
  margin-bottom: 15px;
  font-size: 1.1rem;
  font-weight: 600;
}

.suggestion-section ul {
  margin: 0;
  padding-left: 20px;
}

.suggestion-section li {
  margin-bottom: 10px;
  line-height: 1.5;
  color: #444;
}

/* 达人榜样式 */
.daren-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;
  width: 100%;
  max-width: 100%;
}

.daren-card {
  display: flex;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 16px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.daren-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
  background-color: #fff9fa;
}

.daren-avatar {
  position: relative;
  flex-shrink: 0;
  margin-right: 16px;
}

.daren-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ff2c54;
  background-color: #f5f5f5;
}

.verified-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #2ecc71;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.daren-info {
  flex-grow: 1;
  overflow: hidden;
}

.daren-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 4px;
  color: #333;
}

.daren-category {
  font-size: 14px;
  color: #ff2c54;
  margin: 0 0 8px;
}

.daren-signature {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.daren-stats {
  display: flex;
  justify-content: space-between;
}

.daren-stats .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.daren-stats .stat-label {
  font-size: 12px;
  color: #999;
}

.daren-stats .stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* 近期热门视频样式 */
.recent-videos {
  width: 100%;
  max-width: 2200px;
  margin: 40px auto 0;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 32px rgba(0,0,0,0.08), 0 1.5px 4px rgba(0,0,0,0.03);
  padding: 36px 32px 32px 32px;
}

.recent-videos h3 {
  font-size: 1.45rem;
  margin-bottom: 25px;
  color: #0288d1;
}

.video-buttons {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.video-button {
  flex: 1;
  min-width: 280px;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.video-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  background: #f0f8ff;
  border-color: #90caf9;
}

.video-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
  height: 50px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.video-date {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.video-stats {
  display: flex;
  gap: 15px;
}

.video-likes, .video-comments {
  display: flex;
  align-items: center;
  color: #666;
  font-size: 0.9rem;
}

.like-icon, .comment-icon {
  margin-right: 5px;
  font-style: normal;
}

/* 确保抖音数据榜单页面宽度一致 */
.board-container {
  width: 100%;
  max-width: 2800px;
  margin: 0 auto;
  padding: 40px;
}

.board-content {
  width: 100%;
  max-width: 2800px;
  margin: 0 auto;
  box-sizing: border-box;
}

/* 话题匹配度卡片样式 */
.topic-match-card {
  width: 100%;
  max-width: 2200px;
  margin: 40px auto 0;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 32px rgba(0,0,0,0.08), 0 1.5px 4px rgba(0,0,0,0.03);
  padding: 36px 32px 32px 32px;
}

.topic-match-card h3 {
  font-size: 1.45rem;
  margin-bottom: 25px;
  color: #0288d1;
}

.topic-match-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.match-item {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.match-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.match-video-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
  margin-bottom: 15px;
  border-left: 4px solid #ff2c54;
  padding-left: 10px;
}

.match-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.match-topic {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.match-label, .suggestion-label {
  color: #666;
  font-size: 0.9rem;
}

.match-value {
  font-weight: 500;
  color: #333;
  background: #e3f2fd;
  padding: 4px 10px;
  border-radius: 4px;
}

.match-score {
  padding: 4px 10px;
  border-radius: 4px;
  font-weight: 500;
}

.match-score.high {
  background: #e8f5e9;
  color: #2e7d32;
}

.match-score.medium {
  background: #fff3e0;
  color: #ef6c00;
}

.match-score.low {
  background: #ffebee;
  color: #c62828;
}

.suggestion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
}

.suggestion-tag {
  background: #f0f8ff;
  color: #0288d1;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.suggestion-tag:hover {
  background: #e3f2fd;
}
</style>
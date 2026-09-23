<template>
  <div class="container">
    <h1>抖音数据分析平台</h1>
    <div class="navbar">
      <a href="#" @click.prevent="activePage = 'page-daren'" :class="{ active: activePage === 'page-daren' }">达人榜</a>
      <a href="#" @click.prevent="activePage = 'page-hot'" :class="{ active: activePage === 'page-hot' }">实时热点</a>
      <a href="#" @click.prevent="activePage = 'page-video'" :class="{ active: activePage === 'page-video' }">热门视频榜</a>
    </div>

    <!-- 达人榜 -->
    <div v-if="activePage === 'page-daren'" id="page-daren">
      <h2>可能感兴趣的达人</h2>
      <table class="hot-list" id="daren-table">
        <tr>
          <th>达人</th>
          <th>粉丝数</th>
          <th>昨日销售额</th>
          <th>涨跌幅</th>
        </tr>
        <tr v-for="d in darenData" :key="d.name">
          <td>{{ d.name }}</td>
          <td>{{ d.fans }}</td>
          <td>{{ d.sales }}</td>
          <td>{{ d.change }}</td>
        </tr>
      </table>
      
      <!-- 新增图表容器 -->
      <div class="chart-container" ref="darenGraph"></div>
    </div>

    <!-- 实时热点 -->
    <div v-if="activePage === 'page-hot'" id="page-hot">
      <h2>平台实时热点</h2>
      <div style="display: flex; gap: 40px;">
        <div style="flex:1;">
          <h3>种草热点</h3>
          <ol id="hot-list1">
            <li v-for="(t, i) in hot1" :key="i">{{ i + 1 }}. {{ t }}</li>
          </ol>
        </div>
        <div style="flex:1;">
          <h3>平台热点</h3>
          <ol id="hot-list2">
            <li v-for="(t, i) in hot2" :key="i">{{ i + 1 }}. {{ t }}</li>
          </ol>
        </div>
      </div>
    </div>

    <!-- 热门视频榜 -->
    <div v-if="activePage === 'page-video'" id="page-video">
      <h2>热门视频榜</h2>
      <table class="video-table" id="video-table">
        <tr>
          <th>排名</th>
          <th>视频</th>
          <th>达人</th>
          <th>发布时间</th>
          <th>点赞数</th>
          <th>转发数</th>
          <th>评论数</th>
        </tr>
        <tr v-for="v in videoData" :key="v.rank">
          <td>{{ v.rank }}</td>
          <td>{{ v.title }}</td>
          <td>{{ v.user }}</td>
          <td>{{ v.date }}</td>
          <td>{{ v.likes }}</td>
          <td>{{ v.shares }}</td>
          <td>{{ v.comments }}</td>
        </tr>
      </table>
    </div>

    <!-- 新增图表区域 -->
    <div class="chart-container">
      <div class="chart-item" v-for="(d, index) in sortedDarenData" :key="index">
        <span class="chart-sales">{{ d.sales }}</span>
        <span class="chart-name">{{ d.name }}</span>
        <span class="chart-change">{{ d.change }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  data() {
    return {
      activePage: 'page-daren',
      darenData: [
        { name: "与辉同行", fans: "2,893.3w", sales: "5000w~7500w", change: "+94.36%" },
        { name: "国庄23号蓝月亮限定", fans: "2,276.2w", sales: "2500w~5000w", change: "+48662.48%" },
        { name: "伍娟芳", fans: "395.7w", sales: "2500w~5000w", change: "0.00%" },
        { name: "云上珠宝-20号中午12点", fans: "687.1w", sales: "2500w~5000w", change: "0.00%" },
        { name: "叶海洋", fans: "872.9w", sales: "2500w~5000w", change: "0.00%" }
      ],
      hot1: [
        "华为nova14上手体验", "姜艺潇还原福建三大渔女造型", "华为高分荣耀折叠电脑表现如何",
        "用海棠花大眼打开态夏穿搭", "明星在北京或封打初夏穿搭", "黄子韬给许洋伴侣租件装共享",
        "麦放松一键包裹剥剥玩", "潘长江和田地地京北探店", "男性价值包沙的20礼物清单", "足协部部长鲍春雷520告真礼物"
      ],
      hot2: [
        "广州某科技公司遭网络攻击", "520快乐", "我国从海上发射一箭4星", "潘展乐2冠", "5月LPR下调10个基点",
        "国际乒联国乒王牌软球受损", "WOD世界舞蹈大赛", "韩国山川判新冠病毒拾头", "陈安安汉女报平安", "外交部回应巴巴巴"
      ],
      videoData: [
        { rank: 1, title: "穿搭不论年龄 #反差 #ootd穿搭 #情侣穿搭", user: "牛大爷", date: "05-19 13:35", likes: "17.3w", shares: "11.7w", comments: "2,384" },
        { rank: 2, title: "不是吧！520新鞋在垃圾桶捡到手机", user: "记忆小李", date: "05-19 11:29", likes: "17w", shares: "12w", comments: "4.4w" },
        { rank: 3, title: "孩子天大人又开兵娃告白告白", user: "奇哥人奇", date: "05-19 13:08", likes: "8w", shares: "11.7w", comments: "1,513" },
        { rank: 4, title: "文化不死。杨老师们用爱发电", user: "野猪面条", date: "05-19 09:41", likes: "13.9w", shares: "13.9w", comments: "1.9w" },
        { rank: 5, title: "封打服女大爷", user: "喜心心", date: "05-19 10:29", likes: "9.5w", shares: "2.5w", comments: "2,452" }
      ],
      chartInstance: null,
    };
  },
  computed: {
    sortedDarenData() {
      return [...this.darenData].sort((a, b) => {
        const fansA = parseFloat(a.fans.replace(/,/g, '').replace('w', '0000'));
        const fansB = parseFloat(b.fans.replace(/,/g, '').replace('w', '0000'));
        return fansA - fansB;
      });
    }
  },
  methods: {
    initChart() {
      const chartDom = this.$refs.darenGraph;
      this.chartInstance = echarts.init(chartDom);
      const option = {
        title: {
          text: '达人粉丝数趋势图'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: this.sortedDarenData.map(d => d.name),
          axisLabel: { // 新增 x 轴标签配置
            interval: 0, // 显示所有标签
            rotate: 45, // 旋转标签 45 度
            margin: 10, // 标签与轴线间距
          }
        },
        yAxis: [
          {
            type: 'value',
            name: '销售额',
            position: 'left',
            axisLabel: {
              formatter: '{value}'
            }
          },
          {
            type: 'value',
            name: '涨跌幅',
            position: 'right',
            axisLabel: {
              formatter: '{value}%'
            }
          }
        ],
        series: [
          {
            name: '销售额',
            type: 'bar',
            data: this.sortedDarenData.map(d => parseFloat(d.sales.replace('w~', '').split(' ')[0])),
            yAxisIndex: 0
          },
          {
            name: '涨跌幅',
            type: 'line',
            data: this.sortedDarenData.map(d => parseFloat(d.change.replace('%', ''))),
            yAxisIndex: 1
          }
        ]
      };

      this.chartInstance.setOption(option);
    }
  },
  watch: {
    sortedDarenData: {
      handler(newVal) {
        if (this.chartInstance) {
          const option = {
            xAxis: {
              data: newVal.map(d => d.name)
            },
            series: [
              {
                data: newVal.map(d => parseFloat(d.sales.replace('w~', '').split(' ')[0]))
              },
              {
                data: newVal.map(d => parseFloat(d.change.replace('%', '')))
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
    this.initChart();
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
}

.container {
    max-width: 1200px;
    margin: 40px auto 0 auto;
    padding: 30px 30px 40px 30px;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 6px 32px rgba(0,0,0,0.08), 0 1.5px 4px rgba(0,0,0,0.03);
}

h1 {
    text-align: center;
    color: #0288d1;
    margin-bottom: 40px;
    font-size: 2.2rem;
    letter-spacing: 2px;
}

h2 {
    color: #333;
    margin-bottom: 18px;
    border-left: 4px solid #0288d1;
    padding-left: 12px;
    font-size: 1.3rem;
    font-weight: 600;
}

h3 {
    color: #0288d1;
    font-size: 1.1rem;
    margin-bottom: 10px;
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
    gap: 30px;
    justify-content: center;
    margin-bottom: 35px;
}

.navbar a {
    text-decoration: none;
    color: #333;
    font-weight: bold;
    font-size: 18px;
    padding: 10px 28px;
    border-radius: 8px;
    transition: background 0.2s, color 0.2s;
    background: #f5f5f5;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.navbar a.active, .navbar a:hover {
    background: #0288d1;
    color: #fff;
}

.hidden {
    display: none;
}

.hot-list, .video-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10px;
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.hot-list th, .hot-list td, .video-table th, .video-table td {
    border: 1px solid #f0f0f0;
    padding: 12px 10px;
    text-align: left;
    font-size: 1rem;
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

.trend-graph {
    width: 100%;
    height: 220px;
    background: linear-gradient(135deg, #e3f2fd 0%, #f5f8fa 100%);
    border-radius: 10px;
    margin: 24px 0 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #b0bec5;
    font-size: 1.2rem;
    letter-spacing: 1px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* 新增样式 */
.chart-container {
  width: 600px; /* 根据需要调整宽度 */
  height: 400px; /* 根据需要调整高度 */
  margin-top: 20px;
  background: #f9fbfd;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.chart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: #f9fbfd;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.chart-sales,
.chart-name,
.chart-change {
  font-size: 1rem;
}

.chart-sales {
  color: #4caf50;
}

.chart-change {
  color: #f44336;
}

@media (max-width: 900px) {
    .container {
        padding: 10px;
    }
    .navbar {
        flex-direction: column;
        gap: 10px;
    }
    .section {
        padding: 10px;
    }
    .trend-graph {
        height: 120px;
        font-size: 1rem;
    }
    .hot-list th, .hot-list td, .video-table th, .video-table td {
        padding: 8px 4px;
        font-size: 0.95rem;
    }
}

.right-panel {
  position: fixed;
  top: 50px;
  right: 20px;
  width: 300px;
  height: 300px;
  z-index: 10;
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

@media (max-width: 900px) {
  .right-panel {
    width: 200px;
    height: 200px;
  }
}
</style>

<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center text-lg-h3 mr-6">
         <v-icon class="text-lg-h3 mr-3">mdi-robot-happy</v-icon> MafiaBot
      </div>
      <v-select class="mt-6 mr-4" placeholder="Select a Player" v-model="selected_player_id" :items="players"></v-select>

    </v-app-bar>

    <v-main class="ma-5 mb-0">
      <div v-if="selected_player_id">
          <v-tabs class="mb-3" v-model="cpage">
            <v-tab>Data Over Time</v-tab>
            <v-tab>Single Night Data</v-tab>
          </v-tabs>
        <v-carousel height="auto" hide-delimiters :show-arrows="false" v-model="cpage">
          <v-carousel-item>
            <LineChart class="chart" :chart-data="get_player_data('upto_month_data')" :chart-options="chartOptions" />
          </v-carousel-item>
          <v-carousel-item>
            <LineChart class="chart" :chart-data="get_player_data('single_month_data')" :chart-options="chartOptions" />
          </v-carousel-item>
        </v-carousel>
      </div>
      <div v-else class="align-content-center align-center text-center">
        <h2 STYLE="font-weight: 300">Hi, I am <strong>Martinez</strong> the <strong>MafiaBot</strong></h2>
        <div style="font-weight: 300;" class="mt-2">Please choose a player from the list on the top navbar</div>
        <img class="martinez" src="./assets/martinez.png">
      </div>
    </v-main>
  </v-app>
</template>

<script>
import { Line as LineChart} from 'vue-chartjs/legacy'
import MafiaData from './mafia_data.json'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale)

export default {
  name: 'App',

  components: {
    LineChart
  },
  mounted(){
    // this.$vuetify.theme.dark = true
    // this.$vuetify.theme.themes.dark.primary = '#b45294'
  },
  data: () => ({
    mafia_data: MafiaData,
    selected_player_id: null,
    chartOptions: {
      type: Object,
      default: () => {
      },
      scales: {y: {beginAtZero: true}},
    },
    cpage: 0,
  }),
  methods: {
    get_player_data(data_type){
      let chart_data = {
        labels: [],
        datasets: [
        ]
      }
      let total_points_dataset = {
        label: 'Total Points',
        data: [],
        backgroundColor: "transparent",
        pointBackgroundColor: "rgb(255,255,255)",
        borderColor: this.$vuetify.theme.themes.dark.primary
      }
      for (let [month_number, players_data] of Object.entries(this.mafia_data[data_type])) {
        chart_data.labels.push(month_number)

        if(this.selected_player_id){
          let data = players_data[this.selected_player_id]
          if(data){
            total_points_dataset.data.push(data.total_points || null)
          }else{
            total_points_dataset.data.push(null)
          }
        }
      }

      chart_data.datasets.push(total_points_dataset)
      return chart_data
    }
  },
  computed: {
    players(){
      let users = []
      for (let [username, p] of Object.entries(this.mafia_data.upto_month_data["6"])) {
        users.push({value: username, text: p.name})
      }
      return users
    },
  }
};
</script>

<style>
  .chart canvas{
    max-height: 65vh;
  }
  .martinez{
    max-height: 100vh;
    max-width: 100vw;
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
  }

</style>
<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center text-lg-h3">
         <v-icon class="text-lg-h3 mr-3">mdi-robot-happy</v-icon> MafiaBot
      </div>

      <v-spacer></v-spacer>

      <v-combobox  class="mt-6" placeholder="Select a Player" v-model="selected_player_id" :items="players"></v-combobox>
    </v-app-bar>

    <v-main class="ma-5">
      <div v-if="selected_player_id">
        <h2>Single Month Data</h2>
        <LineChart class="chart" :chart-data="get_player_data('single_month_data')" :chart-options="chartOptions" />

        <h2 class="mt-16">All Data</h2>
        <LineChart class="chart" :chart-data="get_player_data('upto_month_data')" :chart-options="chartOptions" />
      </div>
      <div v-else>
        <h4>Hey its me <strong>Martinez</strong> the Mafia-Bot
        <br>
          Please choose a player from the list on the top right to proceed
        </h4>
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

  data: () => ({
    mafia_data: MafiaData,
    selected_player_id: null,
    chartOptions: {
      type: Object,
      default: () => {}
    }
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
        data: []
      }
      for (let [month_number, players_data] of Object.entries(this.mafia_data[data_type])) {
        chart_data.labels.push(month_number)

        if(this.selected_player_id){
          let data = players_data[this.selected_player_id.value]
          if(data){
            let total_points = data.total_points || null
            total_points_dataset.data.push(total_points)
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
    player_month_on_month_data(){
      return this.get_player_data('upto_month_data')
    }
  }
};
</script>

<style>
  .chart canvas{
    max-height: 80vh;
  }
  .martinez{
    max-height: 90vh;
    max-width: 100vw;
    position: fixed;
    bottom: 0;
  }
</style>
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
        <div>
          <v-select filled label="Graph Type" class="mb-0" placeholder="Graph Type" v-model="graph_type" :items="graph_types"></v-select>
          <v-tabs class="mb-3" style="margin-top: -15px" v-model="cpage">
            <v-tab>Data Over Time</v-tab>
            <v-tab>Single Night Data</v-tab>
          </v-tabs>
        </div>
        <v-carousel height="auto" hide-delimiters :show-arrows="false" v-model="cpage">
          <v-carousel-item>
            <LineChart class="chart" :chart-data="get_player_data('upto_month_data', selected_datasets)" :chart-options="chartOptions" />
          </v-carousel-item>
          <v-carousel-item>
            <LineChart class="chart" :chart-data="get_player_data('single_month_data', selected_datasets)" :chart-options="chartOptions" />
          </v-carousel-item>
        </v-carousel>
      </div>
      <div v-else class="align-content-center align-center text-center">
        <h2 STYLE="font-weight: 300">Hi, I am <strong>Martinez</strong> the <strong>MafiaBot</strong></h2>
        <div style="font-weight: 300;" class="mt-2">Please choose a player from the list on the top navbar</div>
        <img class="martinez" src="./assets/martinez.png">
        <img class="martinez sidetinez" src="./assets/martinez.png">
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
    graph_type: 'total_points',
    graph_types: [
      {text: "Total Points", value: "total_points"},
      {text: "Bonus Points", value: "bonus_points"},
      {text: "Winrates", value: "winrates"}
    ]
  }),
  methods: {
    get_player_data(aggregation_type, data_type_list){
      let chart_data = {
        labels: [],
        datasets: [
        ]
      }
      let possible_data_types =
      {
          total_points: {
            label: 'Total Points',
            data: [],
            backgroundColor: this.$vuetify.theme.themes.dark.primary,
            pointBackgroundColor: "rgb(255,255,255)",
            borderColor: this.$vuetify.theme.themes.dark.primary
          },
          bonus_points: {
            label: 'Bonus Points',
            data: [],
            backgroundColor: this.$vuetify.theme.themes.dark.primary,
            pointBackgroundColor: "rgb(255,255,255)",
            borderColor: this.$vuetify.theme.themes.dark.primary
          },
          total_games_winrate: {
            label: 'Overall Winrate',
            data: [],
            backgroundColor: this.$vuetify.theme.themes.dark.primary,
            pointBackgroundColor: "rgb(255,255,255)",
            borderColor: this.$vuetify.theme.themes.dark.primary
          },
          citizen_games_winrate: {
            label: 'Citizen Winrate',
            data: [],
            backgroundColor:  this.$vuetify.theme.themes.dark.success,
            pointBackgroundColor: "rgb(255,255,255)",
            borderColor: this.$vuetify.theme.themes.dark.success
          },
          mafia_games_winrate: {
            label: 'Mafia Winrate',
            data: [],
            backgroundColor: this.$vuetify.theme.themes.dark.warning,
            pointBackgroundColor: "rgb(255,255,255)",
            borderColor: this.$vuetify.theme.themes.dark.warning
          },
          sheriff_games_winrate: {
            label: 'Sheriff Winrate',
            data: [],
            backgroundColor: "rgb(241,78,219)",
            pointBackgroundColor: "rgb(255,255,255)",
            borderColor: "rgb(241,78,219)"
          },
          don_games_winrate: {
            label: 'Don Winrate',
            data: [],
            backgroundColor: this.$vuetify.theme.themes.dark.error,
            pointBackgroundColor: "rgb(255,255,255)",
            borderColor: this.$vuetify.theme.themes.dark.error
          }
      }
      for (let [month_number, players_data] of Object.entries(this.mafia_data[aggregation_type])) {
        chart_data.labels.push(month_number)

        if(this.selected_player_id){
          let data = players_data[this.selected_player_id]
          if(data){
            data_type_list.forEach(dtl => {
              possible_data_types[dtl].data.push(null || data[dtl])
            })
          }else{
            data_type_list.forEach(dtl => {
              possible_data_types[dtl].data.push(null)
            })
          }
        }
      }

      data_type_list.forEach(dtl => {
       chart_data.datasets.push(possible_data_types[dtl])
      })
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
    selected_datasets(){
      return {
        total_points: ['total_points'],
        bonus_points: ['bonus_points'],
        winrates: ['total_games_winrate', 'citizen_games_winrate', 'mafia_games_winrate', 'sheriff_games_winrate', 'don_games_winrate']
      }[this.graph_type]
    }
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
    /*animation: MoveUpDown 12s linear infinite;*/
  }
  .sidetinez{
    display: none;
    bottom: unset !important;
    left: -100vw;
    transform: rotate(90deg) !important;
    animation: MoveLeftRight 12s linear infinite !important;
    animation-delay: 5s !important;
  }

  @keyframes MoveUpDown {
    0%, 100% {
      bottom: -100vh;
    }
    10% {
      bottom: 0;
    }
    25% {
      bottom: 0;
    }

    75%{
      bottom: -100vh
    }
  }

  @keyframes MoveLeftRight {
    0%, 100% {
      left: -100vw;
    }
    10% {
      left: 0;
    }
    25% {
      left: 0;
    }
    75%{
      left: -100vw;
    }
  }

</style>
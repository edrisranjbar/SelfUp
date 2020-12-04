const TOKEN = 'edri';
const API_URL = `http://127.0.0.1:5000/${TOKEN}/`;
let get_tasks_query = API_URL + "task/all";
let get_results_query = API_URL + "result/all";
let get_categories_query = API_URL + "category/all";
let delete_category = API_URL + "category/delete/";
let delete_task = API_URL + "task/delete/";
let add_task = API_URL + "task/add";
let add_result = API_URL + "result/add";
let add_category = API_URL + "category/add";
let update_task = API_URL + "task/update/";
let update_category = API_URL + "category/update/";

Vue.component('widget-card', {
  props: ['title', 'content', 'icon', 'color'],
  template: '#widget-card-template'
})
Vue.component('error-alert', {
  props: ['error_text'],
  template: '#error-alert-template'
})

let vue = new Vue({
  el: '#app',
  data() {
    return {
      tasks_count: 0,
      categories_count: 0,
      result_count: 0,
      categories: [],
      last_result: null,
      tasks: [],
      results: [],
      show_task_modal: false,
      show_category_modal: false,
      show_result_modal: false,
      current_task_id: null,
      current_category_id: null,
      chartBlur: false,
      errors: []
    }
  },
  methods: {
    updateChart: function () {
      let dates = vue.get_dates();
      let ranks = vue.get_ranks();
      let chartPlace = document.getElementById('myChart').getContext('2d');
      let chart = new Chart(chartPlace, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [{
            label: 'Rank',
            backgroundColor: 'rgba(100, 255, 132,0.5)',
            data: ranks
          }]
        },
      });
    },
    capitalize: function (text) {
      return text.charAt(0).toUpperCase() + text.slice(1);
    },
    showTaskUpdateModal: function (task_id) {
      this.current_task_id = task_id;
      this.show_task_modal = true;
    },
    updateTask: function () {
      let task_name = document.getElementById('new_task_name').value.trim();
      this.find_task(this.current_task_id).name = task_name;
      if (task_name != "") {
        axios.put(update_task + this.current_task_id, `task_name=${task_name}`).then(function (response) {
          console.log(response);
        }).catch(function (error) {
          console.error(error);
          this.errors.push("Can not update task!");
        })
        this.show_task_modal = false;
      }
    },
    updatecategory: function () {
      let category_name = document.getElementById('new_category_name').value.trim();
      let category_description = document.getElementById('new_category_description').value;
      this.find_category(this.current_category_id).name = category_name;
      this.find_category(this.current_category_id).description = category_description;
      this.show_category_modal = false;
      if (category_name != "") {
        axios.put(update_category + this.current_category_id, `name=${category_name}&description=${category_description}`).then(function (response) {
          console.log(response);
        }).catch(function (error) {
          console.error(error);
          this.errors.push("Can not update category!");
        })
      }
    },
    showCategoryUpdateModal: function (category_id) {
      this.current_category_id = category_id;
      this.show_category_modal = true;
    },
    addTask: function () {
      let task_name = document.querySelector('#task_name').value.trim();
      let category_id = document.querySelector('#category').value;
      let last_task_id = this.tasks[this.tasks.length - 1].id;

      if (task_name != "") {
        this.tasks_count++;
        axios.post(add_task, `task_name=${task_name}&category=${category_id}`).then(function (response) {}).catch(function (error) {
          console.error(error);
          vue.errors.push("Can not add Task");
        })
        // add new task to DOM
        this.tasks.push({
          'id': last_task_id + 1,
          'name': task_name,
          'category_id': category_id
        });
      }
    },
    addCategory: function () {
      let category_name = document.querySelector('#category_name').value.trim();
      let description = document.querySelector('#category_description').value;
      let categories_length = this.categories.length - 1;
      let last_category_id;
      if (categories_length > 0) {
        // Getting last category id
        last_category_id = this.categories[categories_length].id;
      } else {
        // There is no category
        last_category_id = 1;
      }
      this.categories.push({
        'id': last_category_id + 1,
        'name': category_name,
        'description': description
      });
      if (category_name != "") {
        this.categories_count++;
        axios.post(add_category, `name=${category_name}&&description=${description}`).then(function (response) {}).catch(function (error) {
          console.error(error);
          this.errors.push("Can not add Category!");
        })
        // Clear data in category name and description
        document.querySelector('#category_name').value = "";
        document.querySelector('#category_description').value = "";
      }
    },
    deleteCategory: function (category) {
      this.categories_count--;
      axios.get(delete_category + category.id).then(function (response) {})
        .catch(function (error) {
          // handle error
          console.error(error);
          this.errors.push("Can not delete Category!");
        })
      let category_id = "category_" + category.id;
      document.getElementById(category_id).style.display = "none";
    },
    deleteTask: function (task) {
      this.tasks_count--;
      axios.get(delete_task + task.id)
        .then(function (response) {
          // handle success
        })
        .catch(function (error) {
          // handle error
          console.error(error);
          this.errors.push("Can not delete Task!");
        })
      let task_id = "task_" + task.id;
      document.getElementById(task_id).style.display = "none";
    },
    get_dates: function () {
      dates = [];
      this.results.forEach(elem => {
        dates.push(elem.date)
      });
      return dates;
    },
    get_ranks: function () {
      ranks = [];
      this.results.forEach(elem => {
        ranks.push(elem.result)
      });
      return ranks;
    },
    find_category: function (category_id) {
      // returns category
      let category = "";
      this.categories.forEach(function (the_category) {
        if (the_category.id == category_id) {
          category = the_category;
        }
      })
      return category;
    },
    find_task: function (task_id) {
      // returns task
      let task = "";
      this.tasks.forEach(function (the_task) {
        if (the_task.id == task_id) {
          task = the_task;
        }
      })
      return task;
    },
    addResult: function () {
      let score = 0;
      let score_step = 100 / this.tasks_count;
      let date = document.getElementById("date").value;
      document.querySelectorAll("#addResultModal input[type=checkbox]").forEach((elem) => {
        if (elem.checked == true) {
          score += score_step;
        }
      })
      // Send score to API
      axios.post(add_result, `result=${score}&date=${date}`).then(function (response) {}).catch(function (error) {
        console.error(error);
        vue.errors.push("Can not add Result");
      })

      this.results.push({
        "date": date,
        "result": score
      });
      this.updateChart();

      // Close Modal
      this.show_result_modal = false;
    },
  },
  mounted() {
    axios.all([
        axios.post(get_tasks_query, {}),
        axios.post(get_results_query),
        axios.post(get_categories_query)
      ])
      .then(axios.spread((taskRes, resultRes, categoryRes) => {
        this.tasks_count = taskRes.data.tasks_count;
        this.categories_count = categoryRes.data.categories_count;
        this.result_count = resultRes.data.results_count;
        if (this.result_count == 0) {
          // blur progress line chart
          this.chartBlur = true;
        }
        this.results = resultRes.data.results;
        let last_result_index = resultRes.data.results.length - 1;
        try {
          this.last_result = resultRes.data.results[last_result_index].result;
        } catch (e) {
          this.last_result = "-";
        }
        let categories = categoryRes.data.categories;
        categories.forEach(element => {
          this.categories.push({
            'name': element.name,
            'id': element.id,
            'description': element.description
          });
        });
        let tasks = taskRes.data.tasks;
        tasks.forEach(element => {
          this.tasks.push({
            'name': element.name,
            'id': element.id,
            'category_id': element.category_id
          });
        });
        this.updateChart();
      })).catch(function (error) {
        console.error(error);
        vue.errors.push("Can not get data from Server! Try again...");
      })
  }
})
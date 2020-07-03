const API_URL = "http://127.0.0.1:5000/"; 
let get_tasks_query = API_URL + "task/all";
let get_results_query = API_URL + "result/all";
let get_categories_query = API_URL + "category/all";
let delete_category = API_URL + "category/delete/";
let delete_task = API_URL + "task/delete/";
let add_task = API_URL + "task/add";
let add_category = API_URL + "category/add";
let update_task = API_URL + "task/update/";
let update_category = API_URL + "category/update/";

Vue.component('widget-card',{
  props: ['title', 'content', 'icon', 'color'],
  template: '#widget-card-template'
})
Vue.component('error-alert',{
  props: ['error_text'],
  template: '#error-alert-template'
})

let vue = new Vue({
    el: '#app',
    data () {
      return {
        tasks_count: null,
        categories_count: null,
        result_count: null,
        categories: [],
        last_result: null,
        tasks: [],
        results: [],
        show_task_modal: false,
        show_category_modal: false,
        current_task_id: null,
        current_category_id: null,
        chartBlur: false,
        errors: []
      }
    },
    methods:{
      capitalize:function(text){
        return text.charAt(0).toUpperCase() + text.slice(1);
      },
      showTaskUpdateModal:function(task_id) {
        this.current_task_id = task_id;
        this.show_task_modal = true;
      },
      updateTask:function() {
        let task_name = document.getElementById('new_task_name').value.trim();
        if(task_name != ""){
          axios.put(update_task+this.current_task_id,`task_name=${task_name}`).then(function(response) {
            console.log(response);
          }).catch(function(error) {
            console.error(error);
            this.errors.push("Can not update task!");
          })
        }
      },
      updatecategory:function() {
        let category_name = document.getElementById('new_category_name').value.trim();
        let category_description = document.getElementById('new_category_description').value;
        if(category_name != ""){
          axios.put(update_category+this.current_category_id,`name=${category_name}&description=${category_description}`).then(function(response) {
            console.log(response);
          }).catch(function(error) {
            console.error(error);
            this.errors.push("Can not update category!");
          })
        }
      },
      showCategoryUpdateModal:function(category_id) {
        this.current_category_id = category_id;
        this.show_category_modal = true;
      },
      addTask:function() {
        let task_name = document.querySelector('#task_name').value.trim();
        let category_id = document.querySelector('#category').value;
        if(task_name != ""){
          axios.post(add_task,`task_name=${task_name}&category=${category_id}`).then(function(response) {
            console.log(response);
          }).catch(function(error) {
            console.error(error);
            vue.errors.push("Can not add Task");
          })
        }
      },
      addCategory:function() {
        let category_name = document.querySelector('#category_name').value.trim();
        let description = document.querySelector('#category_description').value;
        if(category_name != ""){
          axios.post(add_category,`name=${category_name}&&description=${description}`).then(function(response) {
            console.log(response);
          }).catch(function(error) {
            console.error(error);
            this.errors.push("Can not add Category!");
          })
        }
      },
      deleteCategory:function(category){
          axios.get(delete_category+category.id)
          .then(function (response) {
            // handle success
            console.log(response);
          })
          .catch(function (error) {
            // handle error
            console.error(error);
            this.errors.push("Can not delete Category!");
          })          
          let category_id = "category_"+category.id;
          document.getElementById(category_id).style.display = "none";
      },
      deleteTask:function(task){
          axios.get(delete_task+task.id)
          .then(function (response) {
            // handle success
            console.log(response);
          })
          .catch(function (error) {
            // handle error
            console.error(error);
            this.errors.push("Can not delete Task!");
          })          
          let task_id = "task_"+task.id;
          document.getElementById(task_id).style.display = "none";
      },
      get_dates: function(){
        dates = [];
        this.results.forEach(elem=>{dates.push(elem.date)});
        return dates;
      },
      get_ranks: function(){
        ranks = [];
        this.results.forEach(elem=>{ranks.push(elem.result)});
        return ranks;
      },
      find_category: function(category_id){
        // returns category
        let category_name = "";
        this.categories.forEach(function(the_category){
          if(the_category.id == category_id){
            category_name = the_category.name;
            console.log(category_name);
          }
        })
        return category_name;
    },
  },
    mounted () {
        axios.all([
            axios.get(get_tasks_query),
            axios.get(get_results_query),
            axios.get(get_categories_query)
        ])
        .then(axios.spread((taskRes, resultRes, categoryRes) => {
            this.tasks_count = taskRes.data.tasks_count;
            this.categories_count = categoryRes.data.categories_count;
            this.result_count = resultRes.data.results_count;
            if(this.result_count == 0){
              // blur progress line chart
              this.chartBlur = true;
            }
            this.results = resultRes.data.results;
            let last_result_index = resultRes.data.results.length -1;
            try{
              this.last_result = resultRes.data.results[last_result_index].result;
            }
            catch(e){
              this.last_result = "-";
              console.error(e);
            }
            let categories = categoryRes.data.categories;
            categories.forEach(element => {
                this.categories.push({'name': element.name, 'id': element.id, 'description':element.description});
            });
            let tasks = taskRes.data.tasks;
            tasks.forEach(element => {
                this.tasks.push({'name': element.name, 'id': element.id, 'category_id':element.category_id});
            });
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
        })).catch(function(error){
          console.error(error);
          vue.errors.push("Can not get data from Server! Try again...");
        })
    }
})
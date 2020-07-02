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

new Vue({
    el: '#app',
    data () {
      return {
        tasks_count: null,
        categories_count: null,
        result_count: null,
        categories: [],
        last_result: null,
        tasks: [],
        show_task_modal: false,
        show_category_modal: false,
        current_task_id: null,
        current_category_id: null,
      }
    },
    methods:{
      showTaskUpdateModal:function(task_id) {
        this.current_task_id = task_id;
        this.show_task_modal = true;
      },
      updateTask:function() {
        let task_name = document.getElementById('new_task_name').value;
        axios.put(update_task+this.current_task_id,`task_name=${task_name}`).then(function(response) {
          console.log(response);
        }).catch(function(error) {
          console.log(error);
        })
      },
      updatecategory:function() {
        let category_name = document.getElementById('new_category_name').value;
        let category_description = document.getElementById('new_category_description').value;
        axios.put(update_category+this.current_category_id,`name=${category_name}&description=${category_description}`).then(function(response) {
          console.log(response);
        }).catch(function(error) {
          console.log(error);
        })
      },
      showCategoryUpdateModal:function(category_id) {
        this.current_category_id = category_id;
        this.show_category_modal = true;
      },
      addTask:function() {
        let task_name = document.querySelector('#task_name').value;
        axios.post(add_task,`task_name=${task_name}`).then(function(response) {
          console.log(response);
        }).catch(function(error) {
          console.log(error);
        })
      },
      addCategory:function() {
        let category_name = document.querySelector('#category_name').value;
        let description = document.querySelector('#category_description').value;
        axios.post(add_category,`name=${category_name}&&description=${description}`).then(function(response) {
          console.log(response);
        }).catch(function(error) {
          console.log(error);
        })
      },
      deleteCategory:function(category){
          axios.get(delete_category+category.id)
          .then(function (response) {
            // handle success
            console.log(response);
          })
          .catch(function (error) {
            // handle error
            console.log(error);
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
            console.log(error);
          })          
          let task_id = "task_"+task.id;
          document.getElementById(task_id).style.display = "none";
      }
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
            let last_result_index = resultRes.data.results.length -1;
            this.last_result = resultRes.data.results[last_result_index].result;
            let categories = categoryRes.data.categories;
            categories.forEach(element => {
                this.categories.push({'name': element.name, 'id': element.id, 'description':element.description});
            });
            let tasks = taskRes.data.tasks;
            tasks.forEach(element => {
                this.tasks.push({'name': element.name, 'id': element.id});
            });
        }))
    }
})
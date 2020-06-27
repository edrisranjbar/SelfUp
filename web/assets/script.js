let get_tasks_query = "http://127.0.0.1:5000/task/all";
let get_results_query = "http://127.0.0.1:5000/result/all";
let get_categories_query = "http://127.0.0.1:5000/category/all";
let delete_category = "http://127.0.0.1:5000/category/delete/";
let delete_task = "http://127.0.0.1:5000/task/delete/";
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
      }
    },
    methods:{
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
            this.last_result = resultRes.data.results[0].result;
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
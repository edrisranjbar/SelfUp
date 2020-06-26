let get_tasks_query = "http://127.0.0.1:5000/task/all";
let get_results_query = "http://127.0.0.1:5000/result/all";
let get_categories_query = "http://127.0.0.1:5000/category/all";
new Vue({
    el: '#app',
    data () {
      return {
        tasks_count: null,
        categories_count: null,
        result_count: null,
        categories: [],
        last_result: null,
        tasks: []
      }
    },
    methods:{
        // removeCategory: function(item){
            // TODO: remove api call
            // document.getElementById("category_"+item.id).style.display = "none";
        // }
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
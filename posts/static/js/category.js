$('#updateModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var slug = button.data('category-slug') // Extract info from data-* attributes
    var name = button.data('category-name') // Extract info from data-* attributes
    
    var modal = $(this)
    modal.find('.modal-title').text('Update Category ' + name)
    modal.find('.modal-body #id_name').val(name)
    modal.find('.modal-body #id_category_update_slug').val(slug)

})
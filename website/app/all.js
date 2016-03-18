"use strict";

var $ = require('jquery');

/**
 * A really cool thing!
 * @type {{init: App.init}}
 */
var App = {
  init: () => {
    console.log('App initialized.');
  }
};

function deleteAjax(deleteUrl) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: deleteUrl,
      type: 'DELETE'
    })
    .done(result => {
      resolve(result);
    })
    .fail(error => {
      reject(error);
    });
  });
}

// Remove an own plant
$('.remove_own_plant').on('click', event => {
  var confirmAlert = window.confirm('Are you sure you want to remove your own plant?');
  if (confirmAlert) {
    var target = $(event.target);
    var ownPlantId = target.data('own-plant-id');
    var deleteUrl = target.data('delete-url');

    deleteAjax(deleteUrl)
      .then(() => {
        // Just hide the element on success
        $(`#${ownPlantId}`).hide();
      })
      .catch(() => {
        // TODO Error-handling...?
        console.error(222);
      });
  }
});

// Remove a plant
$('.remove_plant').on('click', event => {
  var confirmAlert = window.confirm('Are you sure you want to remove the plant? If you do this, the plants that you\'ve added will be removed as well!');
  if (confirmAlert) {
    var target = $(event.target);
    var ownPlantId = target.data('plant-id');
    var deleteUrl = target.data('delete-url');

    deleteAjax(deleteUrl)
      .then(() => {
        // Just hide the element on success
        $(`#${ownPlantId}`).hide();
      })
      .catch(() => {
        // TODO Error-handling...?
        console.error(333);
      });
  }
});

// Remove a pump
$('.remove_pump').on('click', event => {
  var confirmAlert = window.confirm('Are you sure you want to remove the pump? If you do this, the plants that you\'ve added AND is using this pump will become inactive!');
  if (confirmAlert) {
    var target = $(event.target);
    var pumpId = target.data('pump-id');
    var deleteUrl = target.data('delete-url');

    deleteAjax(deleteUrl)
      .then(() => {
        // Just hide the element on success
        $(`#${pumpId}`).hide();
      })
      .catch(() => {
        // TODO Error-handling...?
        console.error(444);
      });
  }
});

module.exports = App;
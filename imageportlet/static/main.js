/**
 * Your Javascript code goes here.
 *
 * This file is deployed as ++resource++youraddon/main.js on your site
 * and automatically included in merge bundles via jsregistry.xml.
 *
 * More info
 *
 * http://collective-docs.readthedocs.org/en/latest/templates_css_and_javascripts/javascript.html
 *
 */

 /*global window,document*/

(function($) {

    "use strict";

    function rotateBanners() {
        $(".image-portlet-carousel").cycle({timeout:5500});
    }

    $(document).ready(function() {
        rotateBanners();
    });

})(jQuery);


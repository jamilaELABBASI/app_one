/* @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "app_one.ListView";

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            records: [],
        });

        onWillStart(async () => {
           const result = await this.orm.searchRead(
                "property",
                [],
                ["id", "name", "postcode", "date_availability"]
            );
            this.state.records=result;
            console.log(result);
        });
    }


//    async loadRecords(){
//        const result= await this.orm.searchRead("property",[],[]) // lire les donnees apartir du model property
//        console.log(result)
//        this.state.records=result
//        }
}

registry.category("actions").add(
    "app_one.action_list_view",
    ListViewAction
);
















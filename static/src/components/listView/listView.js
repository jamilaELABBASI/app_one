/* @odoo-module */

import { Component,useState,onWillStart,onMounted,onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService,useBus } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "app_one.ListView";

   setup() {
    this.state = useState({ records: [] });
    this.orm = useService("orm");
    this.loadRecords();
    const bus = useService("bus_service");  // Odoo bus
    this.intervalId=setInterval(()=>{this.loadRecords()},3000);
    onWillUnmount(()=>{clearIntervalId(this.intervalId)});

/*
    onWillStart(async () => {
        await this.loadRecords();
    });

    // Écouter le bus
    bus.addEventListener("property_channel", async () => {
        console.log("Changement détecté sur un autre onglet !");
        await this.loadRecords();  // rafraîchir la liste
    });
*/

/*
  // soit on utilise cette method a linterieur du setup() ou on creer une method dans la classe et on lappelle dans setup()
  // cette method permet de recuperer les records properties et les passes au owl xml
        onWillStart(async () => {
           const result = await this.orm.searchRead(
                "property",
                [],
                ["id", "name", "postcode", "date_availability"]
            );
            this.state.records=result;
            console.log(result);
        });
*/
    }

      async loadRecords(){
        const result= await this.orm.searchRead("property",[],[]); // lire les donnees apartir du model property
        console.log(result)
        this.state.records=result
        };

        async createRecord(){
            await this.orm.create("property",
            [{name:"Nouvelle propertie",postcode:"189279"}]
                );
            await this.loadRecords(); // refresh UI
        }


        async deleteRecord(recordId){
            await this.orm.unlink("property",[recordId]);
            await this.loadRecords(); // refresh UI

        }



}



registry.category("actions").add(
    "app_one.action_list_view",
    ListViewAction
);























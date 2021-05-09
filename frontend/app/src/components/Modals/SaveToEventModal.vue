<template>
  <BaseModal :name="this.name" header="Save to Event">
    <TabView class="p-m-1">
      <TabPanel v-for="eventType of existingEvents" :key="eventType.title" :header="eventType.title">
        <div v-for="eventItem of eventType.events" :key="eventItem" class="p-field-radiobutton p-inputgroup">
          <RadioButton :id="eventItem" name="eventItem" :value="eventItem" v-model="selectedEvent"/>
          <label :for="eventItem">{{ eventItem }}</label>
        </div>
        <div class="p-field-radiobutton p-inputgroup">
          <RadioButton id="newEventItem" name="newEventItem" value="New Event" v-model="selectedEvent"/>
          <label for="newEventItem">New Event</label>
        </div>
        <div v-if="newEventSelected" class="p-m-1 p-grid p-fluid p-formgrid">
          <div class="p-field p-col p-m-1">
            <InputText name="newEventName" type="text" v-model="newEventName"/>
            <Textarea v-model="newEventComment" :autoResize="true" rows="5" cols="30" id="newEventComment"
                      placeholder="Add a comment..."/>
            <Dropdown v-model="newEventComment" :options="suggestedComments" :showClear="true"
                      placeholder="Select from a past comment"/>
          </div>
          <div class="p-col-1 p-m-1">
            <Button type="button" icon="pi pi-refresh"
                    class="p-button-outlined p-m-1" @click="autoSetEventName"/>
          </div>
        </div>
      </TabPanel>
    </TabView>
    <template #footer>
      <Button label="Back" icon="pi pi-arrow-left" @click="close" class="p-button-text"/>
      <Button label="Save" icon="pi pi-check" @click="save"  :disabled="!anyEventSelected"/>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal"

export default {
  name: "SaveToEventModal",
  components: { BaseModal },
  computed: {
    anyEventSelected: function () {
      return Boolean(this.selectedEvent);
    },
    newEventSelected: function () {
      return this.selectedEvent === "New Event";
    },
    name() {
      return this.$options.name;
    },
  },
  beforeMount() {
    this.autoSetEventName();
  },
  data() {
    return {
      selectedEvent: null,
      displaySaveToEventModal: false,
      existingEvents: [{'title': 'Open', 'events': ['event1', 'event2']},
        {'title': 'Closed', 'events': ['event3', 'event4']}],
      newEventComment: null,
      newEventName: null,
      suggestedComments: ['this is an old comment', 'and another'],
    }
  },
  methods: {
    autoSetEventName() {
      this.newEventName = "this is a placeholder";
    },
    close() {
      this.selectedEvent = null,
      this.displaySaveToEventModal = false,
      this.existingEvents = [{'title': 'Open', 'events': ['event1', 'event2']},
                             {'title': 'Closed', 'events': ['event3', 'event4']}],
      this.newEventComment = null,
      this.newEventName = null,
      this.$store.dispatch("modals/close", this.name);
    },
    save() {
      this.close();
      this.$store.dispatch("modals/close", 'DispositionModal');
    }
  }
}
</script>
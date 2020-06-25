<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Shops</h1>
      <b-button variant="primary" @click="addNewShop">
        <i class="fas fa-plus" />
      </b-button>
    </div>

    <b-list-group>
      <b-list-group-item v-for="(item, idx) in data" :key="idx">
        <div class="d-flex justify-content-between align-items-center">
          <h2>{{item.name}}</h2>
          <div v-if="adminOrUserCanEdit(item)">
            <b-button variant="success" class="mr-2" size="sm" @click="editShop(item)">
              <i class="fas fa-edit" />
            </b-button>
            <b-button variant="danger" size="sm" @click="removeShop(item)">
              <i class="fas fa-trash" />
            </b-button>
          </div>
        </div>
        <div
          class="font-weight-bold font-italic"
        >Created At: {{(new Date(item.created)).toLocaleString()}}</div>
        <p>{{item.content}}</p>
      </b-list-group-item>
    </b-list-group>

    <b-modal ref="edit-modal" hide-footer title="Shop Info">
      <b-badge variant="danger" block v-show="errorMsg" class="my-2">{{errorMsg}}</b-badge>
      <b-form class="login-form">
        <b-form-group id="input-group-1" label="Shop name:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="form.name"
            type="text"
            required
            placeholder="Enter shop name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-2" label="Shop Content:" label-for="input-2">
          <b-form-textarea
            id="input-2"
            v-model="form.content"
            rows="4"
            required
            placeholder="Enter content"
          ></b-form-textarea>
        </b-form-group>
        <div class="d-flex justify-content-end mt-4">
          <b-button
            class="mr-3"
            variant="outline-success"
            @click="saveData"
            :disabled="posting">
            <b-spinner label="Spinning" variable="success" v-if="posting" class="mr-3"></b-spinner>
            Save
          </b-button>
          <b-button variant="outline-warning" @click="hideModal">Close</b-button>
        </div>
      </b-form>
    </b-modal>
    <b-modal ref="confirm-modal" hide-footer title="Confirm">
      <b-badge variant="danger" block v-show="errorMsg" class="my-2">{{errorMsg}}</b-badge>
      <div class="d-block text-center">
        <h3>Are you sure to remove this item?</h3>
      </div>
      <div class="d-flex justify-content-end mt-4">
        <b-button class="mr-3" variant="outline-danger" @click="confirmDelete" :disabled="posting">
          <b-spinner label="Spinning" variable="success" v-if="posting" class="mr-3"></b-spinner>
          Remove
        </b-button>
        <b-button variant="outline-secondary" @click="closeConfirmModal">Cancel</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  title: 'Главная | anyQuestions?',
  name: 'home',
  data() {
    return {
      id: -1,
      posting: false,
      form: {
        name: '',
        content: '',
      },
    };
  },
  computed: {
    ...mapState('auth', ['userData', 'isSuperUser']),
    ...mapState('shops', ['data', 'errorMsg']),
  },
  mounted() {
    this.getAllShops();
    this.getUserInfo();
  },
  methods: {
    adminOrUserCanEdit(item) {
      return (this.isSuperUser || item.user.split('/')[5] == this.userData.pk);
    },
    getUserInfo() {
      this.$store.dispatch('auth/getAccountDetails');
    },
    getAllShops() {
      this.$store.dispatch('shops/getAllShops');
    },
    addNewShop() {
      this.id = -1;
      this.form.name = '';
      this.form.content = '';
      this.showModal();
    },
    editShop(item) {
      this.id = item.id;
      this.form.name = item.name;
      this.form.content = item.content;
      this.showModal();
    },

    async saveData() {
      this.posting = true;
      if (this.id == -1) {
        const rt = await this.$store.dispatch('shops/addNewShop', this.form);
        this.posting = false;
        if (rt) {
          this.hideModal();
          this.getAllShops();
        }
      } else {
        const rt = await this.$store.dispatch('shops/updateShop', {
          id: this.id,
          data: this.form,
        });
        this.posting = false;
        if (rt) {
          this.hideModal();
          this.getAllShops();
        }
      }
    },
    async confirmDelete() {
      this.posting = true;
      const rt = await this.$store.dispatch('shops/removeShop', this.id);
      this.posting = false;
      if (rt) {
        this.closeConfirmModal();
        this.getAllShops();
      }
    },
    showModal() {
      this.$refs['edit-modal'].show();
    },
    hideModal() {
      this.$refs['edit-modal'].hide();
    },
    removeShop(item) {
      this.id = item.id;
      this.$refs['confirm-modal'].show();
    },
    closeConfirmModal() {
      this.$refs['confirm-modal'].hide();
    },
  },
};
</script>

<style scoped>
</style>

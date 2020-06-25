<template>
  <div class="container py-5">
    <h1 class="mb-4">Users</h1>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">User Id</th>
          <th scope="col">User Name</th>
          <th scope="col">Nick Name</th>
          <th scope="col">Phone</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, idx) in data" :key="idx">
          <th scope="row">{{idx + 1}}</th>
          <td>{{item.username}}</td>
          <td>{{item.first_name + ' ' + item.last_name}}</td>
          <td>{{item.nick_name}}</td>
          <td>{{item.phone}}</td>
          <td>
            <b-button variant="success" class="mr-2" size="sm" @click="editUser(item)">
              <i class="fas fa-edit" />
            </b-button>
            <b-button variant="danger" size="sm" @click="removeUser(item)">
              <i class="fas fa-trash" />
            </b-button>
          </td>
        </tr>
      </tbody>
    </table>

    <b-modal ref="edit-modal" hide-footer title="Shop Info">
      <b-badge variant="danger" block v-show="errorMsg" class="my-2">{{errorMsg}}</b-badge>
      <b-form class="login-form">
        <b-form-group id="input-group-1" label="User ID:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="form.username"
            type="text"
            required
            readonly
            placeholder="Enter user ID"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-2" label="First Name:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="form.first_name"
            type="text"
            required
            placeholder="Enter First Name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Last name:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="form.last_name"
            type="text"
            required
            placeholder="Enter last name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-4" label="Nick name:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="form.nick_name"
            type="text"
            required
            placeholder="Enter nick name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-5" label="Phone number:" label-for="input-5">
          <b-form-input
            id="input-5"
            v-model="form.phone"
            type="text"
            required
            placeholder="Enter phone number"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-end mt-4">
          <b-button
            class="mr-3"
            variant="outline-success"
            @click="saveData"
            :disabled="posting"
          >Save</b-button>
          <b-button variant="outline-warning" @click="hideModal">Close</b-button>
        </div>
      </b-form>
    </b-modal>
    <b-modal ref="confirm-modal" hide-footer title="Confirm">
      <div class="d-block text-center">
        <h3>Are you sure to remove this item?</h3>
      </div>
      <div class="d-flex justify-content-end mt-4">
        <b-button class="mr-3" variant="outline-danger" @click="confirmDelete">Remove</b-button>
        <b-button variant="outline-secondary" @click="closeConfirmModal">Cancel</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'about',
  data() {
    return {
      id: -1,
      posting: false,
      form: {
        username: '',
        first_name: '',
        last_name: '',
        nick_name: '',
        phone: '',
      },
    };
  },
  computed: {
    ...mapState('users', ['data', 'errorMsg']),
  },
  mounted() {
    this.getAllUsers();
  },
  methods: {
    getAllUsers() {
      this.$store.dispatch('users/getAllUsers');
    },
    editUser(item) {
      this.id = item.id;
      this.form.username = item.username;
      this.form.first_name = item.first_name;
      this.form.last_name = item.last_name;
      this.form.nick_name = item.nick_name;
      this.form.phone = item.phone;
      this.showModal();
    },

    async saveData() {
      this.posting = true;
      const rt = await this.$store.dispatch('users/updateUser', {
        id: this.id,
        data: this.form,
      });
      this.posting = false;
      if (rt) {
        this.hideModal();
        this.getAllUsers();
      }
    },
    async confirmDelete() {
      this.posting = true;
      const rt = await this.$store.dispatch('users/removeUser', this.id);
      this.posting = false;
      if (rt) {
        this.closeConfirmModal();
        this.getAllUsers();
      }
    },
    showModal() {
      this.$refs['edit-modal'].show();
    },
    hideModal() {
      this.$refs['edit-modal'].hide();
    },
    removeUser(item) {
      this.id = item.id;
      this.$refs['confirm-modal'].show();
    },
    closeConfirmModal() {
      this.$refs['confirm-modal'].hide();
    },
  },
};
</script>

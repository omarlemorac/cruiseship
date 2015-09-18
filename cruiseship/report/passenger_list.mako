## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
  <style type="text/css">
  ${css}

  thead {
    display: inline-block;
    width: 100%;
    height: 20px;
  }

  tbody {
    height: 200px;
    width: 100%;
    overflow: auto;
  }

  .list_sale_table td {
    border-top: thin solid #EEEEEE;
    text-align:left;
    font-size:10px;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
  }
  .list_sale_table th {
    border-top: thin solid #EEEEEE;
    text-align:center;
    font-size:12px;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
  }

  .flight_info{
    font-size:8px;
  }
  </style>
</head>
<body>
  <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>
  %for departure in objects:
  <% setLang(user.lang) %>
  <table class="list_sale_table">
      <tr>
        <th>Apellido</th>
        <th>Nombre</th>
        <th>T</th>
        <th>MC</th>
        <th>Pasaporte</th>
        <th>Género</th>
        <th>Nacionalidad</th>
        <th>Fecha de Nacimiento</th>
        <th>Restricciones Alimenticias</th>
        <th>Restricciones de Salud</th>
        <th>Asignación de Cabina</th>
        <th colspan="2">Vuelos (Ida/Retorno)</th>
      </tr>
      %for cabin_line in departure.departure_cabin_line_ids:
        %for pax_line in cabin_line.cabin_pax_line_ids:
        <tr>
          <td>${pax_line.pax_id.lastname}</td>
          <td>${pax_line.pax_id.firstname}</td>
          <td>${pax_line.arrange_ticket and 'Si' or 'No'}</td>
          <td>${pax_line.arrange_migration_card and 'Si' or 'No'}</td>
          <td>${pax_line.id_no}</td>
          <td>${pax_line.pax_id.gender}</td>
          <td>${pax_line.pax_id.nationality_id.name}</td>
          <td>${pax_line.pax_id.date_of_birth}</td>
          <td>${pax_line.pax_id.dietary_requirements and pax_line.pax_id.dietary_requirements or '----'}</td>
          <td>${pax_line.pax_id.allergies_medical and pax_line.pax_id.allergies_medical or '----'}</td>
          <td>${cabin_line.cabin_id.name}</td>
          <td style="font-size:8px;">${pax_line.ib_ap_dep_id.name}
            ${formatLang(pax_line.ib_time_dep, date_time=True)} <br /> ${pax_line.ib_ap_arr_id.name}
            ${formatLang(pax_line.ib_time_arr, date_time=True)} <br /> ${pax_line.ib_airline_id.name}/${pax_line.ib_flight_no}</td>
          <td style="font-size:8px;">${pax_line.ob_ap_dep_id.name} 
            ${formatLang(pax_line.ob_time_dep, date_time=True)} <br /> ${pax_line.ob_ap_arr_id.name}
            ${formatLang(pax_line.ob_time_arr, date_time=True)} <br /> ${pax_line.ob_airline_id.name}/${pax_line.ob_flight_no}</td>
        </tr>
        %if pax_line.observations:
        <tr>
          <td colspan="10">${pax_line.observations | carriage_returns}</td>
        </tr>
        %endif
        %endfor
      %endfor
  </table>
  %endfor
</body>
</html>

<%@ page language="java" import="org.json.*"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*"%>
<%
	request.setCharacterEncoding("UTF-8");
%>
<%
	response.setHeader("Access-Control-Allow-Methods", "OPTIONS,POST,GET");
	response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
	response.setHeader("Access-Control-Allow-Origin", "*");
%>
<%
	Connection conn = null;
	String sql;
	//String strAction = request.getParameter("action");

	String url = "jdbc:mysql://139.199.11.57:3306/weapp?"
			+ "user=weapp&password=weapp1&useUnicode=true&characterEncoding=UTF8";

	try {

		Class.forName("com.mysql.jdbc.Driver");// 动态加载mysql驱动

		// 一个Connection代表一个数据库连接

		conn = DriverManager.getConnection(url);
		Statement stmt = conn.createStatement();

		String username = request.getParameter("name");//获取用户名字

		int voteflags = 2;//是否投票标志位

		sql = "SELECT u_make from userinfo where u_name ='" + username + "' ";

		ResultSet res = stmt.executeQuery(sql);

		while (res.next()) {
			
			voteflags = res.getInt(1);
		}//获取是否投票标志位
		
		/*JSON*/
		JSONObject flagListJson = new JSONObject();

		List flagList = new ArrayList();

		JSONObject flags = new JSONObject();

		if (voteflags == 0) {
			
			flags.put("flags", voteflags);//返回判断值给前端 0 尚未投票

			flagList.add(flags);

			flagListJson.put("Voteflag", flagList);

			out.print(flagListJson);

			out.flush();

			/*前端获取id*/
			Integer keys = Integer.parseInt(request.getParameter("id"));

			sql = "SELECT * FROM piaoshu";//获取数据库内容

			ResultSet rs = stmt.executeQuery(sql);//执行结果，返回到rs

			int flag = 0;//保存票数

			while (rs.next()) {

				if (rs.getInt(2) == keys) //判断返回id与数据库对应id相同

					flag = rs.getInt(3);//票数返回

			}

			flag = flag + 1;//票数+1

			sql = " update piaoshu set p_count = '" + flag + "' where p_id ='" + keys + "' ";//更新数据库

			stmt.executeUpdate(sql);

			sql = " update userinfo set u_make = 1 where u_name ='" + username + "' ";//更新数据库

			stmt.executeUpdate(sql);

		} else {
			
			flags.put("flags", voteflags);//返回判断值给前端 1 已投票

			flagList.add(flags);

			flagListJson.put("Voteflag", flagList);

			out.print(flagListJson);

			out.flush();
		}
		stmt.close();

		conn.close();

	} catch (SQLException e) {
		out.println("MySQL操作错误");
		e.printStackTrace();

	} catch (Exception e) {
		out.println("MySQL操作错误");
		e.printStackTrace();

	} finally {

		try {
			conn.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
%>
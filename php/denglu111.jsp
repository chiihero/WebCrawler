<%@page import="org.json.*"%>
<%@ page language="java"  import="java.util.*"  pageEncoding="UTF-8"%>
<%@ page language="java"  import="java.sql.*" %>
<%@ page import="java.text.*" %>
<% 
response.setHeader("Access-Control-Allow-Methods", "OPTIONS,POST,GET");
response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
response.setHeader("Access-Control-Allow-Origin", "*");



	 String driver="com.mysql.jdbc.Driver";
	 String url="jdbc:mysql://139.199.11.57:3306/weapp?";
	 
		Connection conn=null;
		Statement stmt=null;
		ResultSet rsn=null,rse=null;
		String sql;
		boolean flag=true;
		try {
			Class.forName(driver);
			//out.println("JDBC连接MYSQL驱动加载成功");
			conn=DriverManager.getConnection(url,"weapp","weapp1");
			stmt=conn.createStatement();
			//out.println("MYSQL加载成功");
			
			String username=request.getParameter("u_name");
			String userpasswd=request.getParameter("u_passwd");
			String usraction=request.getParameter("action");
				
			//out.println(username);
			//out.println(userpasswd);
			//out.println(useremail);
/*********************************若用户进行登录操作**************************************************/
			//判断用户输入的账号和密码是否为空
			if(username!=null&&(!username.equals(""))&&userpasswd!=null&&(!userpasswd.equals(""))&&(usraction.equals("denglu")))
			{
				sql="select * from userinfo where u_name = '"+username+"'";
				rsn=stmt.executeQuery(sql);
				
				JSONObject denglujson=new JSONObject();
				List denglulist=new ArrayList();
				while(rsn.next()){
					JSONObject denglu=new JSONObject();
					denglu.put("u_name",rsn.getString(1));
					denglu.put("u_id",rsn.getString(2));
					denglu.put("u_passwd",rsn.getString(3));
					denglu.put("u_createdate",rsn.getString(4));
					denglu.put("u_make",rsn.getString(5));
					denglu.put("p_mask",rsn.getString(6));
					denglulist.add(denglu);
				}
				//当前结果集rsn已为空，需重新获取
				rsn=stmt.executeQuery(sql);
				//判断数据库是否存在该用户
				if(rsn.next())
				{
					sql="select * from userinfo where u_name = '"+username+"'";
					rsn=stmt.executeQuery(sql);	
					while(rsn.next()){
			/*********若用户名已注册存在，判断密码是否正确***********/
					if(rsn.getString(3).equals(userpasswd)){
						//密码正确，dengluinfo的值为denglulist的内容
						denglujson.put("dengluinfo",denglulist);
						sql="update userinfo set p_login = 1 where u_name = '"+username+"'";
						stmt.executeUpdate(sql);
					}
					
					else
						//密码不正确，dengluinfo的值为“false”
						denglujson.put("dengluinfo","false");
					break;
					}
				}
		/*************若用户名还没注册，dengluinfo的值为“null”*************/
				else
					denglujson.put("dengluinfo","null");


				out.print(denglujson);
				out.flush();
			}
			
/*********************************若用户进行注册操作*********************************/
			//注册的时候也要判断前端传过来的账号密码是否为空，若为空则不执行
			if(username!=null&& (!username.equals(""))&&userpasswd!=null&&(!userpasswd.equals(""))&&(usraction.equals("zhuce")))
			{
				//查询用户名是否已存在
				sql="select * from userinfo where u_name = '"+username+"'";
				rsn=stmt.executeQuery(sql);
				
				JSONObject zhucejson=new JSONObject();
				List zhucelist=new ArrayList();
				while(rsn.next()){
					JSONObject zhuce=new JSONObject();
					zhuce.put("u_name",rsn.getString(1));
					zhuce.put("u_id",rsn.getString(2));
					zhuce.put("u_passwd",rsn.getString(3));
					zhuce.put("u_createdate",rsn.getString(4));
					zhuce.put("u_make",rsn.getString(5));
					zhuce.put("p_mask",rsn.getString(6));
					zhucelist.add(zhuce);
				}
				String datetime=new SimpleDateFormat("yyyy-MM-dd").format(Calendar.getInstance().getTime());
				//当前结果集rsn已为空，需重新获取
				rsn=stmt.executeQuery(sql);
				
				//out.print(username);
				//out.print(userpasswd);
				//如果获取的用户名不存在，增加新的记录，zhuceinfo的值为“null”
				if(!rsn.next()){
					sql="insert into userinfo(u_name,u_passwd,u_createdate,u_make,p_mask,p_login)values('"+username
							+"','"+userpasswd+"',Current_timestamp,0,0,0)";
					stmt.executeUpdate(sql);
					
					zhucejson.put("zhuceinfo","null");
				}
				//如果存在,zhuceinfo的值为zhucelist的内容，前端显示“用户已存在”
				else{
					zhucejson.put("zhuceinfo",zhucelist);
					
				}		

					out.print(zhucejson);
					out.flush();

			}
/*********************************用户登录时，获取用户的p_login*********************************/								
			if(usraction.equals("getUserinfo")){
				sql="select * from userinfo where p_login = 1";
				rsn=stmt.executeQuery(sql);
				
				JSONObject IsLoginjson=new JSONObject();
				List IsLogin=new ArrayList();
				while(rsn.next()){
					JSONObject Islogin=new JSONObject();
					Islogin.put("u_name",rsn.getString(1));
					Islogin.put("u_id",rsn.getString(2));
					Islogin.put("u_passwd",rsn.getString(3));
					Islogin.put("u_createdate",rsn.getString(4));
					Islogin.put("u_make",rsn.getString(5));
					Islogin.put("p_mask",rsn.getString(6));
					Islogin.put("p_login",rsn.getString(7));
					IsLogin.add(Islogin);
				}
				
				//当前结果集rsn已为空，需重新获取
				//rsn=stmt.executeQuery(sql);
				IsLoginjson.put("IsLogininfo",IsLogin);
				out.print(IsLoginjson);
			}
				
				stmt.close();
				conn.close();
									
			}catch (ClassNotFoundException e) {
			out.print("MYSQL操作错误");
			e.printStackTrace();
		} catch (SQLException e) {
			out.print("MYSQL操作错误");
			e.printStackTrace();
		}finally{

				} 
		

%>
